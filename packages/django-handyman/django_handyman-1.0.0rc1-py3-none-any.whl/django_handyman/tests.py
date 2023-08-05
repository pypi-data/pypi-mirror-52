
from django.test import TestCase
from django.db.models.base import ModelBase
from django.db import connection
from .models import CoreModel
import uuid


class BaseModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create dummy model extending Base, a mixin, if we haven't already.
        if not hasattr(cls, 'model'):
            cls.model = ModelBase(
                '__TestModel__',
                (cls.mixin, ),
                {'__module__': cls.mixin.__module__}
            )

            # Create the schema for our base model. If a schema is already
            # create then let's not create another one.
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls.model)
                super(BaseModelTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(cls.model)
        super(BaseModelTest, cls).tearDownClass()


class CoreModelORMTestCase(BaseModelTest):

    mixin = CoreModel

    def test_orm_soft_delete_queryset(self):

        obj = self.model.objects.create()
        self.assertEqual(self.model.objects.deleted().count(), 0)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.model.objects.all().count(), 1)

        self.model.objects.all().delete()
        self.assertEqual(self.model.objects.deleted().count(), 1)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.model.objects.all().count(), 0)

    def test_orm_soft_delete_on_item(self):
        obj = self.model.objects.create()
        self.assertEqual(self.model.objects.deleted().count(), 0)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.model.objects.all().count(), 1)

        obj.delete()
        self.assertEqual(self.model.objects.deleted().count(), 1)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.model.objects.all().count(), 0)

    def test_orm_undelete_on_item(self):
        obj = self.model.objects.create()
        obj.delete()
        self.assertEqual(self.model.objects.deleted().count(), 1)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.model.objects.all().count(), 0)

        obj.undelete()
        self.assertEqual(self.model.objects.deleted().count(), 0)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.model.objects.all().count(), 1)

    def test_orm_undelete_queryset(self):

        obj = self.model.objects.create()
        self.model.objects.all().delete()
        self.assertEqual(self.model.objects.deleted().count(), 1)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.model.objects.all().count(), 0)

        self.model.objects.get_queryset().undelete()
        self.assertEqual(self.model.objects.deleted().count(), 0)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.model.objects.all().count(), 1)

    def test_orm_soft_delete_queryset_force(self):

        obj = self.model.objects.create()
        self.assertEqual(self.model.objects.deleted().count(), 0)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.model.objects.all().count(), 1)

        self.model.objects.all().delete(force=True)
        self.assertEqual(self.model.objects.deleted().count(), 0)
        self.assertEqual(self.model.objects.count(), 0)
        self.assertEqual(self.model.objects.all().count(), 0)

    def test_orm_soft_delete_on_item_force(self):
        obj = self.model.objects.create()
        self.assertEqual(self.model.objects.deleted().count(), 0)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.model.objects.all().count(), 1)

        obj.delete(force=True)
        self.assertEqual(self.model.objects.deleted().count(), 0)
        self.assertEqual(self.model.objects.count(), 0)
        self.assertEqual(self.model.objects.all().count(), 0)


class ModelDiffMixinORMTestCase(BaseModelTest):

    mixin = CoreModel

    def test_has_changed(self):
        obj = self.model.objects.create()
        # - change something
        obj.uuid = uuid.uuid4()

        self.assertTrue(obj.has_changed)

    def test_diff(self):
        obj = self.model.objects.create()
        old_uuid = obj.uuid
        obj.uuid = uuid.uuid4()

        self.assertTrue(obj.has_changed)
        self.assertIn('uuid', obj.diff)

        # check that first position is the old uuid
        self.assertEqual(obj.diff['uuid'][0], old_uuid)

        # Make sure second position is the new uuid
        self.assertEqual(obj.diff['uuid'][1], obj.uuid)

    def test_changed_fields(self):
        obj = self.model.objects.create()

        # - change something
        obj.uuid = uuid.uuid4()
        self.assertEqual(obj.changed_fields, ['uuid'])

    def test_get_field_diff(self):
        obj = self.model.objects.create()
        old_uuid = obj.uuid
        obj.uuid = uuid.uuid4()

        diff = (obj.get_field_diff('uuid'))
        self.assertEqual(diff[0], old_uuid)
        self.assertEqual(diff[1], obj.uuid)

    def test_save_resets(self):
        obj = self.model.objects.create()
        self.assertTrue(obj.is_created)
        self.assertFalse(obj.is_deleted)
        obj.uuid = uuid.uuid4()

        self.assertTrue(obj.has_changed)
        obj.save()
        self.assertTrue(obj.is_updated)

        self.assertFalse(obj.has_changed)

    def test_initials(self):
        # -- when using the create method
        obj = self.model.objects.create()
        self.assertTrue(obj.is_created)
        self.assertFalse(obj.is_deleted)
        self.assertTrue(obj.is_updated)

        # -- when instanciating a new model

        obj2 = self.model.objects.filter(id=obj.id).first()
        self.assertTrue(obj2.is_created)
        self.assertFalse(obj2.is_deleted)
        self.assertFalse(obj2.is_updated)
        self.assertEqual(obj2.existing_instance, obj)

        # Update something
        obj2.save()
        self.assertTrue(obj2.is_updated)
