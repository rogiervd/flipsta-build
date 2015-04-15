# Properties that are used for generating the documentation.

# To generate the documentation, say "./doc/build.py".

# The directory of the main project.
# There should be "doc" directory inside this directory.
mainProject = 'flipsta'

# The directory of subprojects, i.e. projects that the main project depends on.
# Each of these should be a directory.
# Any project that has a "doc" directory inside its directory will be
# documented.
# Any project that does not will be ignored.
# It is therefore recommended to mention all project here, in case an update
# includes documentation.
subProjects = ['math', 'parse_ll', 'range', 'rime', 'utility', 'meta']

# The human-readable name of the main project.
mainProjectName = 'Flipsta library'

# The copyright.
copyright = '2014-2015 Rogier van Dalen'

# Version of the main project.
version = '0.1'

# The full version, including release tags.
release = '0.1 alpha'

# The path where the documentation will be built.
targetPath = 'doc-build'
