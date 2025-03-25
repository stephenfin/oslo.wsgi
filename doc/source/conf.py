# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -- General configuration ----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'openstackdocstheme',
]

# openstackdocstheme options
openstackdocs_repo_name = 'openstack/oslo.web'
openstackdocs_pdf_link = True
openstackdocs_use_storyboard = False
html_theme = 'openstackdocs'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
copyright = '2026, OpenStack Developers'

# Don't document type hints as they're too noisy
autodoc_typehints = 'none'

# -- Options for HTML output ----------------------------------------------

# Don't let openstackdocstheme insert TOCs automatically.
theme_include_auto_toc = False

# -- Options for LaTeX output ---------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    (
        'index',
        'doc-oslo-web.tex',
        'oslo.web Documentation',
        'OpenStack Foundation',
        'manual',
    ),
]

# Allow deeper levels of nesting for \begin...\end stanzas
latex_elements = {'maxlistdepth': 10}

# Disable usage of xindy https://bugzilla.redhat.com/show_bug.cgi?id=1643664
latex_use_xindy = False
