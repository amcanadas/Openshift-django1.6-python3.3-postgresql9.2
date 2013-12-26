#!/usr/bin/env python
import hashlib, imp, os, sys

# Load the openshift helper library
#lib_path      = os.environ['OPENSHIFT_REPO_DIR'] + 'wsgi/blas/'
#modinfo       = imp.find_module('openshiftlibs', [lib_path])
#openshiftlibs = imp.load_module('openshiftlibs', modinfo[0], modinfo[1], modinfo[2])

# Get database Users
from django.contrib.auth.models import User

usr = User.objects.get(username__exact=os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'])

# Randomly generate a new password and a new salt
# The PASSWORD value below just sets the length (8)
# for the real new password.
#old_keys = { 'SALT': old_salt, 'PASS': '12345678' }
#use_keys = openshiftlibs.openshift_secure(old_keys)

# Encrypt the new password
new_pass = 'Hola'

# Update the user admin password
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'blas'))
usr.set_password(new_pass)
usr.save()

# Print the new password info
print("Django application credentials:\n\tuser: " + os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'] + "\n\t" + new_pass)