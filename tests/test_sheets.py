from dirty_equals import IsAnyStr, IsNumber
from wolpie import GAuth

from core.gsheet.utils import read_current_args


def test_read_current_args(g_auth: GAuth):
    args = read_current_args(g_auth=g_auth)

    assert args.num_days == IsNumber()
    assert args.ticker == IsAnyStr()
