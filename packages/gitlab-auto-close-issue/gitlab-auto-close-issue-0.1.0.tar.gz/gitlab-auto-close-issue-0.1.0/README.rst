.. image:: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue/badges/master/pipeline.svg
   :target: https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue
   :alt: Pipeline Status

.. image:: https://img.shields.io/pypi/l/gitlab-auto-close-issue.svg
   :target: https://pypi.org/project/gitlab-auto-close-issue/
   :alt: PyPI Project License

.. image:: https://img.shields.io/pypi/v/gitlab-auto-close-issue.svg
   :target: https://pypi.org/project/gitlab-auto-close-issue/
   :alt: PyPI Project Version

.. image:: https://readthedocs.org/projects/gitlab-auto-close-issue/badge/?version=latest
   :target: https://gitlab-auto-close-issue.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

gitlab-auto-close-issue
=======================

Python script which will automatically close issues on GitLab for you.

Usage
-----

First you need to create a personal access token, `more information here
<https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_. With the scope ``api``, so it can create the release for you.

.. code-block:: bash

  pip install gitlab-auto-close-issue
  gitlab_auto_close_issue --help

  Usage: gitlab_auto_close_issue [OPTIONS]

    GitLab Auto Close Issue

  Options:
    --private-token TEXT     Private GITLAB token, used to authenticate when
                            calling the MR API.  [required]
    --project-id INTEGER     The project ID on GitLab to create the MR for.
                            [required]
    --project-url TEXT       The project URL on GitLab to create the MR for.
                            [required]
    -i, --issue TEXT         The Issue ID to close.  [required]
    -r, --remove-label TEXT  The labels to remove from (all) the issue(s) before
                            closing it.
    --help                   Show this message and exit.

.. code-block:: bash

    $ gitlab_auto_close_issue --private-token xxx  --project-url https://gitlab.com/hmajid2301/test \
      --project-id 14416075 --issue 1 --remove-label bug

GitLab CI
*********

Set a secret variable in your GitLab project with your private token. Name it ``GITLAB_PRIVATE_TOKEN`` (``CI/CD > Environment Variables``).
This is necessary to close the issue on your behalf.
More information `click here <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_.

Add the following to your ``.gitlab-ci.yml`` file:

.. code-block:: yaml

  stages:
    - post

  publish:release:
    image: registry.gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue
    stage: post
    only:
      - /^release/.*$/
    before_script: []
    script:
      - gitlab_auto_close_issue --issue 1 --remove-label "Doing" --remove-label "To Do"

Changelog
=========

You can find the `changelog here <https://gitlab.com/gitlab-automation-toolkit/gitlab-auto-close-issue/blob/master/CHANGELOG.md>`_.