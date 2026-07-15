from enum import StrEnum
from typing import Any, NotRequired, TypedDict


class AutoRecalc(StrEnum):
    #  definition: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#RecalculationInterval
    RECALCULATION_INTERVAL_UNSPECIFIED = "RECALCULATION_INTERVAL_UNSPECIFIED"
    ON_CHANGE = "ON_CHANGE"
    MINUTE = "MINUTE"
    HOUR = "HOUR"


class NumberFormatType(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#NumberFormatType
    NUMBER_FORMAT_TYPE_UNSPECIFIED = "NUMBER_FORMAT_TYPE_UNSPECIFIED"
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    PERCENT = "PERCENT"
    CURRENCY = "CURRENCY"
    DATE = "DATE"
    TIME = "TIME"
    DATE_TIME = "DATE_TIME"
    SCIENTIFIC = "SCIENTIFIC"


class NumberFormat(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#NumberFormat
    type: NumberFormatType
    pattern: str


class Color(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#Color
    red: int
    green: int
    blue: int


class ThemeColorType(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#ThemeColorType
    THEME_COLOR_TYPE_UNSPECIFIED = "THEME_COLOR_TYPE_UNSPECIFIED"
    TEXT = "TEXT"
    BACKGROUND = "BACKGROUND"
    ACCENT1 = "ACCENT1"
    ACCENT2 = "ACCENT2"
    ACCENT3 = "ACCENT3"
    ACCENT4 = "ACCENT4"
    ACCENT5 = "ACCENT5"
    ACCENT6 = "ACCENT6"
    LINK = "LINK"


class ColorStyle(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#colorstyle
    rgbColor: Color
    themeColor: ThemeColorType


class Style(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#Style
    STYLE_UNSPECIFIED = "STYLE_UNSPECIFIED"
    DOTTED = "DOTTED"
    DASHED = "DASHED"
    SOLID = "SOLID"
    SOLID_MEDIUM = "SOLID_MEDIUM"
    SOLID_THICK = "SOLID_THICK"
    NONE = "NONE"
    DOUBLE = "DOUBLE"


class Border(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#Border
    style: Style
    width: int
    color: Color
    colorStyle: ColorStyle


class Borders(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#Borders
    top: Border
    bottom: Border
    left: Border
    right: Border


class Padding(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#Padding
    top: int
    right: int
    bottom: int
    left: int


class HorizontalAlign(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#HorizontalAlign
    HORIZONTAL_ALIGN_UNSPECIFIED = "HORIZONTAL_ALIGN_UNSPECIFIED"
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


class VerticalAlign(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#VerticalAlign
    VERTICAL_ALIGN_UNSPECIFIED = "VERTICAL_ALIGN_UNSPECIFIED"
    TOP = "TOP"
    MIDDLE = "MIDDLE"
    BOTTOM = "BOTTOM"


class WrapStrategy(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#WrapStrategy
    WRAP_STRATEGY_UNSPECIFIED = "WRAP_STRATEGY_UNSPECIFIED"
    OVERFLOW_CELL = "OVERFLOW_CELL"
    LEGACY_WRAP = "LEGACY_WRAP"
    CLIP = "CLIP"
    WRAP = "WRAP"


class TextDirection(StrEnum):
    # def:https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#TextDirection
    TEXT_DIRECTION_UNSPECIFIED = "TEXT_DIRECTION_UNSPECIFIED"
    LEFT_TO_RIGHT = "LEFT_TO_RIGHT"
    RIGHT_TO_LEFT = "RIGHT_TO_LEFT"


class Link(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#Link
    uri: str


class TextFormat(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#TextFormat
    foregroundColor: Color
    foregroundColorStyle: ColorStyle
    fontFamily: str
    fontSize: int
    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    link: Link


class HyperlinkDisplayType(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#HyperlinkDisplayType
    HYPERLINK_DISPLAY_TYPE_UNSPECIFIED = "HYPERLINK_DISPLAY_TYPE_UNSPECIFIED"
    LINKED = "LINKED"
    PLAIN_TEXT = "PLAIN_TEXT"


class TextRotation(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#TextRotation
    angle: int
    vertical: bool


class CellFormat(TypedDict):
    # definiton: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#CellFormat
    numberFormat: NumberFormat
    backgroundColor: Color
    backgroundColorStyle: ColorStyle
    borders: Borders
    padding: Padding
    horizontalAlignment: HorizontalAlign
    verticalAlignment: VerticalAlign
    wrapStrategy: WrapStrategy
    textDirection: TextDirection
    textFormat: TextFormat
    hyperlinkDisplayType: HyperlinkDisplayType
    textRotation: TextRotation


class IterativeCalculationSettings(TypedDict):
    maxIterations: int
    convergenceThreshold: float


class ThemeColorPair(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#ThemeColorPair
    colorType: ThemeColorType
    color: ColorStyle


class SpreadsheetTheme(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#SpreadsheetTheme
    primaryFontFamily: str
    themeColors: list[ThemeColorPair]


class SpreadsheetProperties(TypedDict):
    # definition: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#SpreadsheetProperties
    title: str
    locale: str
    autoRecalc: AutoRecalc
    timeZone: str
    defaultFormat: CellFormat
    iterativeCalculationSettings: IterativeCalculationSettings
    spreadsheetTheme: SpreadsheetTheme
    importFunctionsExternalUrlAccessAllowed: bool


class ErrorType(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#ErrorType
    ERROR_TYPE_UNSPECIFIED = "ERROR_TYPE_UNSPECIFIED"
    ERROR = "ERROR"
    NULL_VALUE = "NULL_VALUE"
    DIVIDE_BY_ZERO = "DIVIDE_BY_ZERO"
    VALUE = "VALUE"
    REF = "REF"
    NAME = "NAME"
    NUM = "NUM"
    N_A = "N_A"
    LOADING = "LOADING"


class ErrorValue(TypedDict):
    # ref: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#ErrorValue
    type: ErrorType
    message: str


class ExtendedValue(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#ExtendedValue
    numberValue: float
    stringValue: str
    boolValue: bool
    formulaValue: str
    errorValue: ErrorValue


class TextFormatRun(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#TextFormatRun
    startIndex: int
    format: TextFormat


class ConditionType(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#ConditionType
    CONDITION_TYPE_UNSPECIFIED = "CONDITION_TYPE_UNSPECIFIED"
    NUMBER_GREATER = "NUMBER_GREATER"
    NUMBER_GREATER_THAN_EQ = "NUMBER_GREATER_THAN_EQ"
    NUMBER_LESS = "NUMBER_LESS"
    NUMBER_LESS_THAN_EQ = "NUMBER_LESS_THAN_EQ"
    NUMBER_EQ = "NUMBER_EQ"
    NUMBER_NOT_EQ = "NUMBER_NOT_EQ"
    NUMBER_BETWEEN = "NUMBER_BETWEEN"
    NUMBER_NOT_BETWEEN = "NUMBER_NOT_BETWEEN"
    TEXT_CONTAINS = "TEXT_CONTAINS"
    TEXT_NOT_CONTAINS = "TEXT_NOT_CONTAINS"
    TEXT_STARTS_WITH = "TEXT_STARTS_WITH"
    TEXT_ENDS_WITH = "TEXT_ENDS_WITH"
    TEXT_EQ = "TEXT_EQ"
    TEXT_IS_EMAIL = "TEXT_IS_EMAIL"
    TEXT_IS_URL = "TEXT_IS_URL"
    DATE_EQ = "DATE_EQ"
    DATE_AFTER = "DATE_AFTER"
    DATE_ON_OR_BEFORE = "DATE_ON_OR_BEFORE"
    DATE_BETWEEN = "DATE_BETWEEN"
    DATE_NOT_BETWEEN = "DATE_NOT_BETWEEN"
    DATE_ON_OR_AFTER = "DATE_ON_OR_AFTER"
    DATE_IS_VALID = "DATE_IS_VALID"
    ONE_OF_RANGE = "ONE_OF_RANGE"
    BLANK = "BLANK"
    NOT_BLANK = "NOT_BLANK"
    ONE_OF_LIST = "ONE_OF_LIST"
    CUSTOM_FORMULA = "CUSTOM_FORMULA"
    TEXT_NOT_EQ = "TEXT_NOT_EQ"
    DATE_NOT_EQ = "DATE_NOT_EQ"
    BOOLEAN = "BOOLEAN"
    FILTER_EXPRESSION = "FILTER_EXPRESSION"
    DATE_BEFORE = "DATE_BEFORE"


class RelativeDate(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#RelativeDate
    RELATIVE_DATE_UNSPECIFIED = "RELATIVE_DATE_UNSPECIFIED"
    PAST_YEAR = "PAST_YEAR"
    PAST_MONTH = "PAST_MONTH"
    PAST_WEEK = "PAST_WEEK"
    YESTERDAY = "YESTERDAY"
    TODAY = "TODAY"
    TOMORROW = "TOMORROW"


class ConditionValue(TypedDict):
    # ref :https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#ConditionValue
    relativeDate: RelativeDate
    userEnteredValue: str


class BooleanCondition(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#BooleanCondition
    type: ConditionType
    values: list[ConditionValue]


class DataValidationRule(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#DataValidationRule
    condition: BooleanCondition
    inputMessage: str
    strict: bool
    showCustomUi: bool


class PivotGroupMetadata(TypedDict):
    # def :https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#PivotGroupValueMetadata
    value: ExtendedValue
    collapsed: bool


class SortOrder(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#SortOrder
    SORT_ORDER_UNSPECIFIED = "SORT_ORDER_UNSPECIFIED"
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class PivotGroupSortValueBucket(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#PivotGroupSortValueBucket
    valuesIndex: int
    buckets: list[ExtendedValue]


class ManualRuleGroup(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#ManualRuleGroup
    groupName: ExtendedValue
    items: list[ExtendedValue]


class ManualRule(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#ManualRule
    groups: list[ManualRuleGroup]


class HistogramRule(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#histogramrule
    interval: float
    start: float
    end: float


class DateTimeRuleType(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#DateTimeRuleType
    DATE_TIME_RULE_TYPE_UNSPECIFIED = "DATE_TIME_RULE_TYPE_UNSPECIFIED"
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    HOUR_MINUTE = "HOUR_MINUTE"
    HOUR_MINUTE_AMPM = "HOUR_MINUTE_AMPM"
    DAY_OF_WEEK = "DAY_OF_WEEK"
    DAY_OF_YEAR = "DAY_OF_YEAR"
    DAY_OF_MONTH = "DAY_OF_MONTH"
    DAY_MONTH = "DAY_MONTH"
    MONTH = "MONTH"
    QUARTER = "QUARTER"
    YEAR = "YEAR"
    YEAR_MONTH = "YEAR_MONTH"
    YEAR_QUARTER = "YEAR_QUARTER"
    YEAR_MONTH_DAY = "YEAR_MONTH_DAY"


class DateTimeRule(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#DateTimeRule
    type: DateTimeRuleType


class PivotGroupRule(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#PivotGroupRule
    manualRule: ManualRule
    histogramRule: HistogramRule
    dateTimeRule: DateTimeRule


class PivotGroupLimit(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#PivotGroupLimit
    countLimit: int
    applyOrder: int


class DataSourceColumnReference(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#DataSourceColumnReference
    name: str


class PivotGroup(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#PivotGroup
    showTotals: bool
    valueMetadata: list[PivotGroupMetadata]
    sortOrder: SortOrder
    valueBucket: PivotGroupSortValueBucket
    repeatHeadings: bool
    label: str
    groupRule: PivotGroupRule
    groupLimit: PivotGroupLimit
    sourceColumnOffset: int
    dataSourceColumnReference: DataSourceColumnReference


class PivotFilterCriteria(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#pivotfiltercriteria
    visibleStrings: list[str]
    condition: BooleanCondition
    visibleByDefault: bool


class PivotFilterSpec(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#pivotfilterspec
    filterCriteria: PivotFilterCriteria
    columnOffsetIndex: int
    dataSourceColumnReference: DataSourceColumnReference


class PivotValueSummarizeFunction(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#PivotValueSummarizeFunction
    PIVOT_STANDARD_VALUE_FUNCTION_UNSPECIFIED = "PIVOT_STANDARD_VALUE_FUNCTION_UNSPECIFIED"
    SUM = "SUM"
    COUNTA = "COUNTA"
    COUNT = "COUNT"
    COUNTUNIQUE = "COUNTUNIQUE"
    AVERAGE = "AVERAGE"
    MAX = "MAX"
    MIN = "MIN"
    MEDIAN = "MEDIAN"
    PRODUCT = "PRODUCT"
    STDEV = "STDEV"
    STDEVP = "STDEVP"
    VAR = "VAR"
    VARP = "VARP"
    CUSTOM = "CUSTOM"
    NONE = "NONE"


class PivotValueCalculatedDisplayType(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#PivotValueCalculatedDisplayType
    PIVOT_VALUE_CALCULATED_DISPLAY_TYPE_UNSPECIFIED = "PIVOT_VALUE_CALCULATED_DISPLAY_TYPE_UNSPECIFIED"
    PERCENT_OF_ROW_TOTAL = "PERCENT_OF_ROW_TOTAL"
    PERCENT_OF_COLUMN_TOTAL = "PERCENT_OF_COLUMN_TOTAL"
    PERCENT_OF_GRAND_TOTAL = "PERCENT_OF_GRAND_TOTAL"


class PivotValue(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#PivotValue
    summarizeFunction: PivotValueSummarizeFunction
    name: str
    calculatedDisplayType: PivotValueCalculatedDisplayType
    sourceColumnOffset: int
    formula: str
    dataSourceColumnReference: DataSourceColumnReference


class PivotValueLayout(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#PivotValueLayout
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"


class DataExecutionState(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#DataExecutionState
    DATA_EXECUTION_STATE_UNSPECIFIED = "DATA_EXECUTION_STATE_UNSPECIFIED"
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    CANCELLING = "CANCELLING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class DataExecutionErrorCode(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#DataExecutionErrorCode
    DATA_EXECUTION_ERROR_CODE_UNSPECIFIED = "DATA_EXECUTION_ERROR_CODE_UNSPECIFIED"
    TIMED_OUT = "TIMED_OUT"
    TOO_MANY_ROWS = "TOO_MANY_ROWS"
    TOO_MANY_COLUMNS = "TOO_MANY_COLUMNS"
    TOO_MANY_CELLS = "TOO_MANY_CELLS"
    ENGINE = "ENGINE"
    PARAMETER_INVALID = "PARAMETER_INVALID"
    UNSUPPORTED_DATA_TYPE = "UNSUPPORTED_DATA_TYPE"
    DUPLICATE_COLUMN_NAMES = "DUPLICATE_COLUMN_NAMES"
    INTERRUPTED = "INTERRUPTED"
    CONCURRENT_QUERY = "CONCURRENT_QUERY"
    OTHER = "OTHER"
    TOO_MANY_CHARS_PER_CELL = "TOO_MANY_CHARS_PER_CELL"
    DATA_NOT_FOUND = "DATA_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    MISSING_COLUMN_ALIAS = "MISSING_COLUMN_ALIAS"
    OBJECT_NOT_FOUND = "OBJECT_NOT_FOUND"
    OBJECT_IN_ERROR_STATE = "OBJECT_IN_ERROR_STATE"
    OBJECT_SPEC_INVALID = "OBJECT_SPEC_INVALID"
    DATA_EXECUTION_CANCELLED = "DATA_EXECUTION_CANCELLED"


class DataExecutionStatus(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#DataExecutionStatus
    state: DataExecutionState
    errorCode: DataExecutionErrorCode
    errorMessage: str
    lastRefreshTime: str


class GridRange(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#GridRange
    sheetId: int
    startRowIndex: int
    endRowIndex: int
    startColumnIndex: int
    endColumnIndex: int


class PivotTable(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#PivotTable
    rows: list[PivotGroup]
    columns: list[PivotGroup]
    criteria: dict[int, PivotFilterCriteria]
    filterSpecs: list[PivotFilterSpec]
    values: list[PivotValue]
    valueLayout: PivotValueLayout
    dataExecutionStatus: DataExecutionStatus
    source: GridRange
    dataSourceId: str


class DataSourceTableColumnSelectionType(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#DataSourceTableColumnSelectionType
    DATA_SOURCE_TABLE_COLUMN_SELECTION_TYPE_UNSPECIFIED = "DATA_SOURCE_TABLE_COLUMN_SELECTION_TYPE_UNSPECIFIED"
    SELECTED = "SELECTED"
    SYNC_ALL = "SYNC_ALL"


class FilterCriteria(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#FilterCriteria
    hiddenValues: list[str]
    condition: BooleanCondition
    visibleBackgroundColor: Color
    visibleBackgroundColorStyle: ColorStyle
    visibleForegroundColor: Color
    visibleForegroundColorStyle: ColorStyle


class FilterSpec(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#FilterSpec
    filterCriteria: FilterCriteria
    columnIndex: int
    dataSourceColumnReference: DataSourceColumnReference


class SortSpec(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/other#sortspec
    sortOrder: SortOrder
    foregroundColor: Color
    foregroundColorStyle: ColorStyle
    backgroundColor: Color
    backgroundColorStyle: ColorStyle
    dimensionIndex: int
    dataSourceColumnReference: DataSourceColumnReference


class DataSourceTable(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#datasourcetable
    dataSourceId: str
    columnSelectionType: DataSourceTableColumnSelectionType
    columns: list[DataSourceColumnReference]
    filterSpecs: list[FilterSpec]
    sortSpecs: list[SortSpec]
    rowLimit: int
    dataExecutionStatus: DataExecutionStatus


class DataSourceFormula(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#DataSourceFormula
    dataSourceId: str
    dataExecutionStatus: DataExecutionStatus


class DisplayFormat(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#displayformat
    DISPLAY_FORMAT_UNSPECIFIED = "DISPLAY_FORMAT_UNSPECIFIED"
    DEFAULT = "DEFAULT"
    LAST_NAME_COMMA_FIRST_NAME = "LAST_NAME_COMMA_FIRST_NAME"
    EMAIL = "EMAIL"


class RichLinkProperties(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#richlinkproperties
    uri: str
    mimeType: str


class PersonProperties(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#personproperties
    email: str
    displayFormat: DisplayFormat
    richLinkProperties: RichLinkProperties


class Chip(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#Chip
    personProperties: PersonProperties


class ChipRun(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#chiprun
    startIndex: int
    chip: Chip


class CellData(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#CellData
    userEnteredValue: ExtendedValue
    effectiveValue: ExtendedValue
    formattedValue: str
    userEnteredFormat: CellFormat
    effectiveFormat: CellFormat
    hyperlink: str
    note: str
    testFormatRuns: list[TextFormatRun]
    dataValidation: DataValidationRule
    pivotTable: PivotTable
    dataSourceTable: DataSourceTable
    dataSourceFormula: DataSourceFormula
    chipRuns: list[ChipRun]


class RowData(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#RowData
    values: list[CellData]


class DeveloperMetadataLocationType(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.developerMetadata#DeveloperMetadata.DeveloperMetadataLocationType
    DEVELOPER_METADATA_LOCATION_TYPE_UNSPECIFIED = "DEVELOPER_METADATA_LOCATION_TYPE_UNSPECIFIED"
    ROW = "ROW"
    COLUMN = "COLUMN"
    SHEET = "SHEET"
    SPREADSHEET = "SPREADSHEET"


class Dimension(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/Dimension
    DIMENSION_UNSPECIFIED = "DIMENSION_UNSPECIFIED"
    ROWS = "ROWS"
    COLUMNS = "COLUMNS"


class DimensionRange(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/DimensionRange
    sheetId: str
    dimension: Dimension
    startIndex: int
    endIndex: int


class DeveloperMetadataLocation(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.developerMetadata#DeveloperMetadata.DeveloperMetadataLocation
    locationType: DeveloperMetadataLocationType
    spreadsheet: bool
    sheetId: int
    dimensionRange: DimensionRange


class DeveloperMetadataVisibility(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.developerMetadata#DeveloperMetadata.DeveloperMetadataVisibility
    DEVELOPER_METADATA_VISIBILITY_UNSPECIFIED = "DEVELOPER_METADATA_VISIBILITY_UNSPECIFIED"
    DOCUMENT = "DOCUMENT"
    PROJECT = "PROJECT"


class DeveloperMetadata(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.developerMetadata#DeveloperMetadata
    metadataId: int
    metadataKey: str
    metadataValue: str
    location: DeveloperMetadataLocation
    visibility: DeveloperMetadataVisibility


class DimensionProperties(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#dimensionproperties
    hiddenByFilter: bool
    hiddenByUser: bool
    pixelSize: int
    developerMetadata: list[DeveloperMetadata]
    dataSourceColumnReference: DataSourceColumnReference


class GridData(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#GridData
    startRow: int
    startColumn: int
    rowData: list[RowData]
    rowMetadata: list[DimensionProperties]
    columnMetadata: list[DimensionProperties]


class BooleanRule(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#booleanrule
    condition: BooleanCondition
    format: CellFormat


class InterpolationPointType(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#interpolationpointtype
    INTERPOLATION_POINT_TYPE_UNSPECIFIED = "INTERPOLATION_POINT_TYPE_UNSPECIFIED"
    MIN = "MIN"
    MAX = "MAX"
    NUMBER = "NUMBER"
    PERCENT = "PERCENT"
    PERCENTILE = "PERCENTILE"


class InterpolationPoint(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#interpolationpoint
    color: Color
    ColorStyle: ColorStyle
    type: InterpolationPointType
    value: str


class GradientRule(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#gradientrule
    minpoint: InterpolationPoint
    midpoint: InterpolationPoint
    maxpoint: InterpolationPoint


class ConditionalFormatRule(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#ConditionalFormatRule
    ranges: list[GridRange]
    booleanRule: BooleanRule
    gradientRule: GradientRule


class FilterView(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#filterview
    filterViewId: int
    title: str
    range: GridRange
    namedRangeId: str
    tableId: str
    sortSpecs: list[SortOrder]
    criteria: dict[int, FilterCriteria]
    filterSpecs: list[FilterSpec]


class Editors(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#editors
    users: list[str]
    groups: list[str]
    domainUsersCanEdit: bool


class ProtectedRange(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#ProtectedRange
    protectedRangeId: int
    range: list[GridRange]
    namedRangeId: str
    tableId: str
    description: str
    warningOnly: bool
    requestingUserCanEdit: bool
    unprotectedRanges: list[GridRange]
    editors: Editors


class BasicFilter(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#basicfilter
    range: GridRange
    tableId: str
    sortSpecs: list[SortSpec]
    criteria: dict[int, FilterCriteria]
    filterSpecs: list[FilterSpec]


class TextPosition(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/charts#TextPosition
    horizontalAlignment: HorizontalAlign


class DataSourceChartProperties(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/charts#datasourcechartproperties
    dataSourceId: str
    dataExecutionStatus: DataExecutionStatus


class ChartHiddenDimensionStrategy(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/charts#ChartHiddenDimensionStrategy
    CHART_HIDDEN_DIMENSION_STRATEGY_UNSPECIFIED = "CHART_HIDDEN_DIMENSION_STRATEGY_UNSPECIFIED"
    SKIP_HIDDEN_ROWS_AND_COLUMNS = "SKIP_HIDDEN_ROWS_AND_COLUMNS"
    SKIP_HIDDEN_ROWS = "SKIP_HIDDEN_ROWS"
    SKIP_HIDDEN_COLUMNS = "SKIP_HIDDEN_COLUMNS"
    SHOW_ALL = "SHOW_ALL"


class BasicChartSpec(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/charts#BasicChartSpec
    pass


class ChartSpec(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/charts#ChartSpec
    title: str
    altText: str
    titleTextFormat: TextFormat
    titleTextPosition: TextPosition
    subtitle: str
    subtitleTextFormat: TextFormat
    subtitleTextPosition: TextPosition
    fontName: str
    maximized: bool
    backgroundColor: Color
    backgroundColorStyle: ColorStyle
    dataSourceChartProperties: DataSourceChartProperties
    filterSpecs: list[FilterSpec]
    sortSpecs: list[SortSpec]
    hiddenDimensionStrategy: ChartHiddenDimensionStrategy
    basicChart: BasicChartSpec


class EmbeddedChart(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/charts#embeddedchart
    chartId: str
    spec: ChartSpec


class BandingProperties(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#BandingProperties
    headerColor: Color
    headerColorStyle: ColorStyle
    firstBandColor: Color
    firstBandColorStyle: ColorStyle
    secondBandColor: Color
    secondBandColorStyle: ColorStyle
    footerColor: Color
    footerColorStyle: ColorStyle


class BandedRange(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#BandedRange
    bandedRangeId: int
    range: GridRange
    rowProperties: BandingProperties
    columnProperties: BandingProperties


class DimensionGroup(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#DimensionGroup
    range: DimensionRange
    depth: int
    collapsed: bool


class SlicerSpec(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#SlicerSpec
    dataRange: GridRange
    filterCriteria: FilterCriteria
    columnIndex: int
    applyToPivotTables: bool
    title: str
    textFormat: TextFormat
    backgroundColor: Color
    backgroundColorStyle: ColorStyle
    horizontalAlignment: HorizontalAlign


class Slicer(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#Slicer
    slicerId: int
    spec: SlicerSpec


class ColumnType(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#ColumnType
    COLUMN_TYPE_UNSPECIFIED = "COLUMN_TYPE_UNSPECIFIED"
    TEXT = "TEXT"
    NUMERIC = "NUMERIC"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"


class TableColumnDataValidationRule(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#TableColumnDataValidationRule
    rule: DataValidationRule


class TableColumnProperties(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#TableColumnProperties
    id: int
    label: str
    columnType: ColumnType
    dataValidationRule: TableColumnDataValidationRule


class TableRowsProperties(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#TableRowsProperties
    headerRowIndex: int


class Table(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#Table
    tableId: int
    range: GridRange
    headerValues: list[str]
    columns: list[TableColumnProperties]
    dataExecutionStatus: DataExecutionStatus
    tableRows: TableRowsProperties
    borderColor: Color
    borderColorStyle: ColorStyle


class SheetType(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#SheetType
    SHEET_TYPE_UNSPECIFIED = "SHEET_TYPE_UNSPECIFIED"
    GRID = "GRID"
    OBJECT = "OBJECT"
    DATA_SOURCE = "DATA_SOURCE"


class GridProperties(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#GridProperties
    rowCount: int
    columnCount: int
    frozenRowCount: int
    frozenColumnCount: int
    hideGridlines: bool
    rowGroupControlAfter: bool
    columnGroupControlAfter: bool


class DataSourceColumn(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#DataSourceColumn
    reference: DataSourceColumnReference
    formula: str


class DataSourceSheetProperties(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#DataSourceSheetProperties
    dataSourceId: str
    columns: list[DataSourceColumn]
    dataExecutionStatus: DataExecutionStatus


class SheetProperties(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#SheetProperties
    sheetId: int
    title: str
    index: int
    sheetType: SheetType
    gridProperties: GridProperties
    hidden: bool
    tabColor: Color
    tabColorStyle: ColorStyle
    rightToLeft: bool
    dataSourceSheetProperties: DataSourceSheetProperties


class Sheet(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/sheets#Sheet
    properties: SheetProperties
    data: list[GridData]
    merges: list[GridRange]
    conditionalFormats: list[ConditionalFormatRule]
    filterViews: list[FilterView]
    protectedRanges: list[ProtectedRange]
    basicFilter: BasicFilter
    charts: list[EmbeddedChart]
    bandedRanges: list[BandedRange]
    developerMetadata: list[DeveloperMetadata]
    rowGroups: list[DimensionGroup]
    columnGroups: list[DimensionGroup]
    slicers: list[Slicer]
    tables: list[Table]


class NamedRange(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#NamedRange
    namedRangeId: str
    name: str
    range: GridRange


class BigQueryQuerySpec(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#BigQueryQuerySpec
    rawQuery: str


class BigQueryTableSpec(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#BigQueryTableSpec
    tableProjectId: str
    tableId: str
    datasetId: str


class BigQueryDataSourceSpec(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#BigQueryDataSourceSpec
    projectId: str
    querySpec: BigQueryQuerySpec
    tableSpec: BigQueryTableSpec


class LookerDataSourceSpec(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#LookerDataSourceSpec
    instanceUri: str
    model: str
    explore: str


class DataSourceParameter(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#DataSourceParameter
    name: str
    namedRangeId: str
    range: GridRange


class DataSourceSpec(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#DataSourceSpec
    parameters: list[DataSourceParameter]
    bigQuery: BigQueryDataSourceSpec
    looker: LookerDataSourceSpec


class DataSource(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#DataSource
    dataSourceId: str
    spec: DataSourceSpec
    calculatedColumns: list[DataSourceColumn]
    sheetId: int


class TimeOfDay(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#TimeOfDay
    hours: int
    minutes: int
    seconds: int
    nanos: int


class DayOfWeek(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#DayOfWeek
    DAY_OF_WEEK_UNSPECIFIED = "DAY_OF_WEEK_UNSPECIFIED"
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class DataSourceRefreshDailySchedule(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#DataSourceRefreshDailySchedule
    startTime: TimeOfDay


class DataSourceRefreshWeeklySchedule(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#DataSourceRefreshWeeklySchedule
    startTime: TimeOfDay
    daysOfWeek: list[DayOfWeek]


class DataSourceRefreshMonthlySchedule(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#DataSourceRefreshMonthlySchedule
    startTime: TimeOfDay
    daysOfMonth: list[int]


class Interval(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#Interval
    startTime: str
    endTime: str


class DataSourceRefreshScope(StrEnum):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#DataSourceRefreshScope
    DATA_SOURCE_REFRESH_SCOPE_UNSPECIFIED = "DATA_SOURCE_REFRESH_SCOPE_UNSPECIFIED"
    ALL_DATA_SOURCES = "ALL_DATA_SOURCES"


class DataSourceRefreshSchedule(TypedDict):
    # def: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#DataSourceRefreshSchedule
    enabled: bool
    refreshScope: DataSourceRefreshScope
    nextRun: Interval
    dailySchedule: DataSourceRefreshDailySchedule
    weeklySchedule: DataSourceRefreshWeeklySchedule
    monthlySchedule: DataSourceRefreshMonthlySchedule


class SpreadsheetResource(TypedDict):
    # definition: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#Spreadsheet
    spreadsheetId: str
    properties: SpreadsheetProperties
    sheets: list[Sheet]
    namedRanges: list[NamedRange]
    spreadsheetUrl: str
    developerMetadata: list[DeveloperMetadata]
    dataSources: list[DataSource]
    dataSourceSchedules: list[DataSourceRefreshSchedule]


class ValueRenderOption(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/ValueRenderOption
    FORMATTED_VALUE = "FORMATTED_VALUE"
    UNFORMATTED_VALUE = "UNFORMATTED_VALUE"
    FORMULA = "FORMULA"


class DateTimeRenderOption(StrEnum):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/DateTimeRenderOption
    SERIAL_NUMBER = "SERIAL_NUMBER"
    FORMATTED_STRING = "FORMATTED_STRING"


class ValueRange(TypedDict):
    # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values#ValueRange
    range: NotRequired[str]
    majorDimension: Dimension
    values: list


class ValueInputOption(StrEnum):
    INPUT_VALUE_OPTION_UNSPECIFIED = "INPUT_VALUE_OPTION_UNSPECIFIED"
    RAW = "RAW"
    USER_ENTERED = "USER_ENTERED"


class UpdateValuesResponse(TypedDict):
    spreadsheetId: str
    updatedRange: str
    updatedRows: int
    updatedColumns: int
    updatedCells: int
    updatedData: NotRequired[ValueRange]


class GHttpErrorDetails(TypedDict):
    error_details: str
    reason: str
    resp: dict[str, Any]
    status_code: int
    uri: str
    traceback: str  # My own thingy
