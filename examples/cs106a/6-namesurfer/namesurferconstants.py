"""Configuration constants for NameSurfer.

Frankly, the Java usage of an interface holding only constants is a wretched
subversion of the meaning of an interface, so instead we make these constants
module-scope.
"""

# The width of the application window.
APPLICATION_WIDTH = 800;

# The height of the application window.
APPLICATION_HEIGHT = 600;

# The name of the file containing the data.
NAMES_DATA_FILE = "names-data.txt";

# The first decade in the database.
START_DECADE = 1900;

# The number of decades.
NDECADES = 11;

# The maximum rank in the database.
MAX_RANK = 1000;

# The number of pixels to reserve at the top and bottom.
GRAPH_MARGIN_SIZE = 20;
