from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _ug
from easy_thumbnails.fields import ThumbnailerImageField
from . import hardcode


# Custom user which inherits from an AbstractUser and uses the code in
#  backends.py to authenticate and validate permissions
class CustomUser(AbstractUser):
    middle_name = models.CharField(
        max_length=hardcode.user_middlename_length,
        blank=True,
        null=True,
        verbose_name=_ug('Middle Name')
    )
    mothers_name = models.CharField(
        max_length=hardcode.user_mothersname_length,
        blank=True,
        null=True,
        verbose_name=_ug('Mothers Name')
    )
    nickname = models.CharField(
        max_length=hardcode.user_nickname_length,
        blank=True,
        null=True,
        verbose_name=_ug('Nickname')
    )
    avatar = ThumbnailerImageField(
        upload_to=hardcode.user_avatar_upload,
        default=hardcode.user_default_photo,
        blank=True,
        null=True,
        verbose_name=_ug('Profile picture')
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name=_ug('Birthday')
    )
    gender = models.IntegerField(
        default=hardcode.GENDER_UNKNOWN,
        choices=hardcode.GENDER,
        blank=True,
        null=True,
        verbose_name=_ug('Gender')
    )
    step = models.IntegerField(
        default=hardcode.STEP_UNKNOWN,
        choices=hardcode.STEPS,
        blank=False,
        null=False,
        verbose_name=_ug('Step')
    )
    occupation = models.CharField(
        max_length=hardcode.user_occupation_length,
        blank=True,
        null=True,
        verbose_name=_ug('Occupation')
    )
    edition_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_ug('Last edition date')
    )

    class Meta:
        verbose_name = _ug('User')
        verbose_name_plural = _ug('Users')
        permissions = (
            ('query_customuser', 'Can query User'),
            ('list_customuser', 'Can list User'),
        )

    def save(self, *args, **kwargs):
        if self.pk is None:
            avatar = self.avatar
            self.avatar = None
            super(CustomUser, self).save(*args, **kwargs)
            self.avatar = avatar
        super(CustomUser, self).save(*args, **kwargs)

    def delete(self, *args):
        if self.active is False:
            super(CustomUser, self).delete(*args)
        else:
            self.active = False
            self.save()

    def __str__(self):
        return "%s - %s %s" % (self.username, self.first_name, self.last_name)

    def get_full_name(self):
        full_name = '%s %s %s %s' % (self.first_name, self.middle_name,
                                     self.last_name, self.mothers_name)
        return full_name.strip()

    def get_username(self):
        return "%s" % self.username

    def get_nickname(self):
        return "%s" % self.nickname

    def get_short_name(self):
        if self.nickname is None or self.nickname == '':
            return "%s" % self.username
        return self.get_nickname()


class Category(models.Model):
    name = models.CharField(
        max_length=hardcode.category_name_length,
        blank=False,
        null=False,
        verbose_name=_ug('Name')
    )
    edition_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_ug('Last edition date')
    )
    hidden = models.BooleanField(
        default=False,
        blank=True,
        null=False,
        verbose_name=_ug('Hidden')
    )

    class Meta:
        verbose_name = _ug('Category')
        verbose_name_plural = _ug('Categories')
        permissions = (
            ('query_category', 'Can query Category'),
            ('list_category', 'Can list Categories'),
        )

    def delete(self, *args):
        if self.hidden is True:
            super(Category, self).delete(*args)
        else:
            self.hidden = True
            self.save()


class Cluster(models.Model):
    name = models.CharField(
        max_length=hardcode.cluster_name_length,
        blank=False,
        null=False,
        verbose_name=_ug('Name')
    )
    category = models.ForeignKey(
        Category,
        blank=False,
        null=False,
        verbose_name=_ug('Category')
    )
    edition_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_ug('Last edition date')
    )
    hidden = models.BooleanField(
        default=False,
        blank=True,
        null=False,
        verbose_name=_ug('Hidden')
    )

    class Meta:
        verbose_name = _ug('Cluster')
        verbose_name_plural = _ug('Clusters')
        permissions = (
            ('query_cluster', 'Can query Cluster'),
            ('list_cluster', 'Can list Clusters'),
        )

    def delete(self, *args):
        if self.hidden is True:
            super(Cluster, self).delete(*args)
        else:
            self.hidden = True
            self.save()


class IsometricImage(models.Model):
    image = ThumbnailerImageField(
        upload_to=hardcode.isometric_image_upload,
        default=hardcode.isometric_image_photo,
        blank=False,
        null=False,
        verbose_name=_ug('Isometric Image')
    )
    cluster = models.ForeignKey(
        Cluster,
        blank=False,
        null=False,
        verbose_name=_ug('Cluster')
    )
    edition_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_ug('Last edition date')
    )
    hidden = models.BooleanField(
        default=False,
        blank=True,
        null=False,
        verbose_name=_ug('Hidden')
    )

    class Meta:
        verbose_name = _ug('Isometric Image')
        verbose_name_plural = _ug('Isometric Images')
        permissions = (
            ('query_isometricimage', 'Can query Isometric Image'),
            ('list_isometricimage', 'Can list Isometric Images'),
        )

    def save(self, *args, **kwargs):
        if self.pk is None:
            avatar = self.avatar
            self.avatar = None
            super(IsometricImage, self).save(*args, **kwargs)
            self.avatar = avatar
        super(IsometricImage, self).save(*args, **kwargs)

    def delete(self, *args):
        if self.hidden is True:
            super(IsometricImage, self).delete(*args)
        else:
            self.hidden = True
            self.save()


class Question(models.Model):
    text = models.CharField(
        max_length=hardcode.question_text_length,
        blank=False,
        null=False,
        verbose_name=_ug('Text')
    )
    edition_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_ug('Last edition date')
    )
    hidden = models.BooleanField(
        default=False,
        blank=True,
        null=False,
        verbose_name=_ug('Hidden')
    )

    class Meta:
        verbose_name = _ug('Question')
        verbose_name_plural = _ug('Questions')
        permissions = (
            ('query_question', 'Can query Question'),
            ('list_question', 'Can list Questions'),
        )

    def delete(self, *args):
        if self.hidden is True:
            super(Question, self).delete(*args)
        else:
            self.hidden = True
            self.save()


class Answer(models.Model):
    text = models.CharField(
        max_length=hardcode.answer_text_length,
        blank=False,
        null=False,
        verbose_name=_ug('Text')
    )
    category = models.ForeignKey(
        Category,
        blank=False,
        null=False,
        verbose_name=_ug('Category')
    )
    question = models.ForeignKey(
        Question,
        blank=False,
        null=False,
        verbose_name=_ug('Question')
    )
    edition_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_ug('Last edition date')
    )
    hidden = models.BooleanField(
        default=False,
        blank=True,
        null=False,
        verbose_name=_ug('Hidden')
    )

    class Meta:
        verbose_name = _ug('Answer')
        verbose_name_plural = _ug('Answers')
        permissions = (
            ('query_answer', 'Can query Answer'),
            ('list_answer', 'Can list Answers'),
        )

    def delete(self, *args):
        if self.hidden is True:
            super(Answer, self).delete(*args)
        else:
            self.hidden = True
            self.save()
