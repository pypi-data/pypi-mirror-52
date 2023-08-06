from django.db import models
from django.utils import timezone
import uuid
from .mixins import ModelDiffMixin


class BaseQuerySet(models.QuerySet):
    """
    A base queryset that has some extended functionality from django
    """

    def delete(self, force=False):
        """
        Fakes a queryset .delete() and instead adds the time an item has
        been deleted

        Keyword Arguments:
            force {bool} -- Flag on whether to use a hard delete and delete
            the item from the database, or to do a soft delete instead
        """
        # Delete all items anyway
        if force:
            super().delete()

        # Perform a soft delete instead
        else:
            return self.update(deleted=timezone.now())

    def deleted(self):
        """
        Gets all objects that are deleted
        """
        return self.filter(deleted__isnull=False)

    def active(self):
        '''
        Return all stock that is not deleted
        '''
        return self.filter(deleted__isnull=True)

    def undelete(self):
        return self.update(deleted=None)


class BaseManager(models.Manager):

    """
    A base queryset that has some extended functionality from django
    """

    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)

    def deleted(self):
        """
        Returns only deleted items        
        """
        return self.get_queryset().deleted()

    def all(self):
        """
        When using MODEL.objects.all() -> Instead of getting all objects,
        rather only get objects that are not deleted.
        """
        return self.get_queryset().active()


class CoreModel(ModelDiffMixin, models.Model):
    """
    A base model that has repeatable behaviour that
    all other models should inherit
    """

    # -- Set the object manager
    objects = BaseManager()

    # -- Default fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    deleted = models.DateTimeField(null=True, blank=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4)

    class Meta:
        abstract = True

    def delete(self, force=False):
        """Performs a delete on the object

        Keyword Arguments:
            force {bool} -- Flag on whether to use a hard delete and delete
            the item from the database, or to do a soft delete instead
        """

        if force:
            # Perform a hard delete
            super().delete()

        else:
            # Perform a soft delete
            self.deleted = timezone.now()
            self.save()

    def undelete(self):
        """Remove the `deleted` value and undo the soft delete"""

        self.deleted = None
        self.save()

    def save(self, *a, **k):
        # -- Run pre save
        self.pre_save()

        # -- Run actual save
        super().save(*a, **k)

        # -- update our variables
        self._is_created = self.existing_instance is None
        self._is_updated = True

        # run post save
        self.post_save()

    def pre_save(self):
        """
        Pre Save Trigger, you can use this to change instance variables
        or even add/alter or run pre-save signals
        """
        pass

    def post_save(self):
        """
        Post Save Trigger, called after .save() and can be used for any 
        post processing. Similar to signals.
        """
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_updated = False
        self.is_new_instance = self.pk is None

    @property
    def is_deleted(self):
        return bool(self.deleted)

    @property
    def is_created(self):
        return bool(self.existing_instance)

    @property
    def is_updated(self):
        return self._is_updated

    @property
    def existing_instance(self):
        def _call():
            if self.pk:
                return self.__class__.objects.get(pk=self.pk)
        return _call()


# class ImageGallery(models.Model):
#     image = models.ImageField(
#         upload_to='', blank=True,
#         null=True
#     )
#     caption = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return self.image.url
