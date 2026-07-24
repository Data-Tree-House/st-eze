from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "http://127.0.0.1:8000/api/v1/stock/price"
MAX_WORKERS = 10  # adjust based on how much load the local API can handle

TICKERS = """
JSE:BHG
JSE:BTI
JSE:ANH
JSE:PRX
JSE:CFR
JSE:GLN
JSE:ANG
JSE:AGL
JSE:GFI
JSE:NPN
JSE:CPI
JSE:FSR
JSE:SBK
JSE:VAL
JSE:MTN
JSE:VOD
JSE:IMP
JSE:ABG
JSE:S32
JSE:SLM
JSE:HAR
JSE:SSW
JSE:DSY
JSE:SHP
JSE:NHM
JSE:NPH
JSE:BID
JSE:NED
JSE:OUT
JSE:RMI
JSE:KIO
JSE:NRP
JSE:RNI
JSE:REM
JSE:INP
JSE:PPH
JSE:SOL
JSE:PAN
JSE:MNP
JSE:BVT
JSE:OMU
JSE:CLS
JSE:EXX
JSE:GRT
JSE:CCO
JSE:QLT
JSE:TBS
JSE:APN
JSE:WHL
JSE:MTM
JSE:DRD
JSE:SNT
JSE:RDF
JSE:ARI
JSE:MRP
JSE:HMN
JSE:INL
JSE:AVI
JSE:SRE
JSE:N91
JSE:KST
JSE:VKE
JSE:BOX
JSE:FFB
JSE:DCP
JSE:RES
JSE:TKG
JSE:TFG
JSE:OPA
JSE:HYP
JSE:PMR
JSE:TRU
JSE:SRI
JSE:MTH
JSE:KRO
JSE:ADH
JSE:APH
JSE:CML
JSE:NTC
JSE:DTC
JSE:LTE
JSE:WBC
JSE:NY1
JSE:LHC
JSE:GTC
JSE:EQU
JSE:TGA
JSE:MSP
JSE:BYI
JSE:PIK
JSE:SPP
JSE:AHB
JSE:WBO
JSE:OMN
JSE:JSE
JSE:ATT
JSE:HCI
JSE:GND
JSE:ITE
JSE:RLO
JSE:ARL
JSE:SAC
JSE:SUI
JSE:AFE
JSE:SAP
JSE:AFH
JSE:ISO
JSE:RBX
JSE:PPC
JSE:SDO
JSE:CVW
JSE:SSS
JSE:AEL
JSE:BAT
JSE:THA
JSE:BLU
JSE:IPF
JSE:RCL
JSE:TSG
JSE:HET
JSE:CAA
JSE:OCE
JSE:CLI
JSE:DIB
JSE:EMI
JSE:RFG
JSE:HDC
JSE:HIL
JSE:NT1
JSE:RBO
JSE:AFT
JSE:KAP
JSE:SEA
JSE:FBR
JSE:SPG
JSE:SYG
JSE:SBP
JSE:CAT
JSE:EXP
JSE:LEW
JSE:ACS
JSE:CHP
JSE:NPK
JSE:KP2
JSE:OCT
JSE:BEL
JSE:SUR
JSE:KAL
JSE:SHG
JSE:TDH
JSE:OAO
JSE:ORN
JSE:JBL
JSE:IVT
JSE:MPT
JSE:CSB
JSE:MRF
JSE:PPE
JSE:YYLBEE
JSE:LBR
JSE:SDL
JSE:EOH
JSE:CLH
JSE:MDI
JSE:CMH
JSE:CTA
JSE:ZZD
JSE:ZED
JSE:EPE
JSE:GML
JSE:NVS
JSE:HPR
JSE:SCD
JSE:ART
JSE:QFH
JSE:BWN
JSE:ACL
JSE:OAS
JSE:APF
JSE:EPS
JSE:BRN
JSE:EMN
JSE:MMP
JSE:TEX
JSE:AHA
JSE:DNB
JSE:UPL
JSE:TPC
JSE:BCF
JSE:YRK
JSE:TCP
JSE:MTA
JSE:GPL
JSE:SNV
JSE:ACT
JSE:MST
JSE:SSK
JSE:MCZ
JSE:WEZ
JSE:ENX
JSE:ADR
JSE:PBG
JSE:RMH
JSE:HLM
JSE:NWL
JSE:CGR
JSE:AEG
JSE:FGL
JSE:SEP
JSE:TON
JSE:NRL
JSE:VUN
JSE:SOLBE1
JSE:4SI
JSE:ISA
JSE:PMV
JSE:TTO
JSE:GAI
JSE:AME
JSE:RTN
JSE:CKS
JSE:PPR
JSE:DLT
JSE:BRT
JSE:TMT
JSE:ISB
JSE:SOH
JSE:HUG
JSE:WSL
JSE:EMH
JSE:CMO
JSE:KBO
JSE:AON
JSE:NCS
JSE:TRL
JSE:CAC
JSE:RHB
JSE:MRI
JSE:TLM
JSE:BIK
JSE:SEB
JSE:LAB
JSE:RNG
JSE:GLI
JSE:RTO
JSE:AOO
JSE:EUZ
JSE:EEL
JSE:VIS
JSE:ADW
JSE:ELI
JSE:MED
""".split()


def make_session():
    session = requests.Session()
    retry = Retry(
        total=5,  # max retry attempts
        backoff_factor=1,  # 1s, 2s, 4s, 8s... when no Retry-After
        status_forcelist=[429, 500, 502, 503, 504],
        respect_retry_after_header=True,  # honors Retry-After if the server sends it
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# One session per thread would be safer, but a single shared Session
# is fine here since requests' Session is thread-safe for simple GETs.
session = make_session()


def fetch_price(ticker_str):
    exchange, ticker = ticker_str.split(":", 1)
    params = {"ticker": ticker, "exchange": exchange}
    headers = {"accept": "application/json"}
    try:
        response = session.get(BASE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return {"ticker": ticker_str, "status": "ok", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"ticker": ticker_str, "status": "error", "error": str(e)}


def main():
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_ticker = {executor.submit(fetch_price, t): t for t in TICKERS}
        for future in as_completed(future_to_ticker):
            result = future.result()
            results.append(result)
            if result["status"] == "ok":
                print(f"[OK]    {result['ticker']}: {result['data']}")
            else:
                print(f"[ERROR] {result['ticker']}: {result['error']}")

    ok_count = sum(1 for r in results if r["status"] == "ok")
    err_count = len(results) - ok_count
    print(f"\nDone. {ok_count} succeeded, {err_count} failed out of {len(results)} total.")
    return results


if __name__ == "__main__":
    main()
