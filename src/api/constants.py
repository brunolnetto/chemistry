# Description: Constants used in the project

# Time horizon to check for item metrics
DEFAULT_AGE = 12

# Array with valid age months
VALID_AGE_MONTHS = [6, 12, 24, 36]

# Array with valid data file extensions
datafile_extensions = ['.csv', '.xls', '.xlsx']

# Descrição de tipos válidos para leitura de arquivo
VALID_CONTENT_TYPES = [
    "text/csv", 
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
]
VALID_FILE_TYPES = [
    'csv', 'xls', 'xlsx'
]

# Número máximo de arquivos de log
MAX_LOG_FILES = 10
MAX_LOG_FOLDER_SIZE_MB = 10

# Username requirements
USERNAME_MIN_LENGTH = 3

# Password requirements 
PASSWORD_REQUIREMENTS_DICT = {
    "min_length": 8,
    "min_uppercase": 1,
    "min_lowercase": 1,
    "min_digits": 1,
    "min_special_chars": 1,
}
