#!/bin/bash

RELEASE=$1

VERSION=$(echo "$RELEASE" | sed 's/\([0-9]*\.[0-9]*\).*/\1/')

# Update docs version
sed -i "s/\(version = \).*/\1'"$VERSION"'/;s/\(release = \).*/\1'"$RELEASE"'/" 'docs/conf.py'

# Update setup.py version
sed -i "s/\(version=\).*/\1'"$RELEASE"',/" 'setup.py'

# Update __init__ version
sed -i "s/\(__version__ = \).*/\1'"$RELEASE"'/" 'pylux/__init__.py'
