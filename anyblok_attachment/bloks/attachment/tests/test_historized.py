# This file is a part of the AnyBlok / Attachment api project
#
#    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from anyblok_mixins.mixins.exceptions import (
    ForbidUpdateException, ForbidDeleteException)
from os import urandom


@pytest.mark.usefixtures('rollback_registry')
class TestHistorized:

    def test_query_only_history(self, rollback_registry):
        registry = rollback_registry
        document = registry.Attachment.Document.Latest.insert()
        history = registry.Attachment.Document.History.insert(
            uuid=document.uuid, version_number=100000)
        assert registry.Attachment.Document.History.query().filter_by(
            uuid=document.uuid).one() is history

    def test_update(self, rollback_registry):
        registry = rollback_registry
        file_ = urandom(100)
        document = registry.Attachment.Document.insert(file=file_)
        document.historize_a_copy()
        with pytest.raises(ForbidUpdateException):
            document.previous_version.data = {'other': 'data'}
            registry.flush()

    def test_delete(self, rollback_registry):
        registry = rollback_registry
        file_ = urandom(100)
        document = registry.Attachment.Document.insert(file=file_)
        document.historize_a_copy()
        with pytest.raises(ForbidDeleteException):
            document.previous_version.delete()
            registry.flush()
