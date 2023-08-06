from django.db import models

from schools.models import School, Faculty
from common import common_helpers

def get_first_faculty():
    return Faculty.objects.all()[0].pk



class QIManager(models.Manager):

    # get a QI based on the pk
    def get_qi(self, pk):
        return self.get(pk=pk)

    def get_all_qis(self):
        return self.all().order_by('pk')

    def get_qis_from_pk_list(self, qi_ids):

        return self.filter(
            pk__in=qi_ids
        )



class QI(models.Model):
    qi_number = models.CharField(max_length=5, default='x.x')
    qi_text = models.CharField(max_length=150)
    qi_long_description = models.CharField(max_length=1500, default='QI long description text')

    objects = QIManager()

    def __str__(self):
        return self.qi_number + ': ' + self.qi_text

class NIFPriorityManager(models.Manager):

    def get_nif_priority(self, nif_priority_pk):

        return self.get(
            pk=nif_priority_pk
        )

class NIFPriority(models.Model):

    nif_priority = models.CharField(max_length=125)
    objects = NIFPriorityManager()

    def __str__(self):
        return self.nif_priority


class NIFDriverManager(models.Manager):

    def get_nif_driver(self, nif_driver_pk):

        return self.get(
            pk=nif_driver_pk
        )

class NIFDriver(models.Model):

    nif_driver = models.CharField(max_length=50)
    objects = NIFDriverManager()

    def __str__(self):
        return self.nif_driver


class ThemeManager(models.Manager):

    # get a Theme based on the pk
    def get_theme(self, pk):
        return self.get(pk=pk)

    # get all of the themes in a QI
    def get_qi_themes(self, qi):
        return self.filter(qi=qi).order_by('theme_number')

    def get_departmental_qi_themes_teacher(self, qi):
        all_themes = self.get_qi_themes(qi)
        exclude_themes = []
        for theme in all_themes:
            has_teacher_theme_features = ThemeFeature.objects.has_theme_features(theme, 'Teacher', True)

            if has_teacher_theme_features is False:
                exclude_themes.append(theme)

        dept_only_themes = all_themes.exclude(pk__in=[et.pk for et in exclude_themes])
        return dept_only_themes


class Theme(models.Model):
    qi = models.ForeignKey(QI, on_delete=models.CASCADE)
    theme_number = models.CharField(max_length=10, default='x.x')
    theme_name = models.CharField(max_length=200)
    theme_long_description = models.CharField(max_length=1500, default='Theme long description text')
    nif_priority = models.ForeignKey(NIFPriority, on_delete=models.CASCADE, null=True, blank=True)
    nif_driver = models.ForeignKey(NIFDriver, on_delete=models.CASCADE, null=True, blank=True)

    objects = ThemeManager()

    def __str__(self):
        return self.theme_name


class HGIOURSThemeManager(models.Manager):

    # get a HGIOURS Theme based on the pk
    def get_hgiours_theme(self, pk):
        return self.get(pk=pk)

    def get_all_hgiours_themes(self):
        return self.all()

    def get_themes_from_pk_list(self, selected_hgiours_theme_keys):

        return self.filter(
            pk__in=selected_hgiours_theme_keys
        )


class HGIOURSTheme(models.Model):
    theme_number = models.CharField(max_length=1, default='1')
    theme_name = models.CharField(max_length=30, default='HGIOURS Theme')

    objects = HGIOURSThemeManager()

    def __str__(self):
        return self.theme_name


class ThemeFeatureManager(models.Manager):

    # does the theme (with user type) have any features?
    def has_theme_features(self, theme, user_type, is_departmental):
        theme_feature_count = self.filter(
            theme=theme,
            user_type=user_type,
            is_departmental=is_departmental
        ).count()

        return theme_feature_count > 0

    # get the theme features for a theme and a given user_type
    def get_theme_features(self, theme, user_type, is_departmental):

        return self.filter(
            theme=theme,
            user_type=user_type,
            is_departmental=is_departmental
        ).order_by('pk')

    def get_theme_features_school_type(self, theme, user_type, school_type, is_departmental):

        theme_features = self.get_theme_features(theme, user_type, is_departmental)

        if school_type == 'Primary':
            return theme_features.exclude(secondary_only=True)
        elif school_type == 'Secondary':
            return theme_features.exclude(primary_only=True)
        else:
            return theme_features

    def get_theme_feature_ids(self, theme_id, user_type, is_departmental):

        theme = Theme.objects.get_theme(theme_id)
        return self.filter(
            theme=theme,
            user_type=user_type,
            is_departmental=is_departmental
        ).values_list('pk', flat=True)


    def get_theme_feature(self, feature_pk):

        return self.get(
            pk=feature_pk
        )

    def get_theme_features_as_outcomes(self, base_plan_priority, school, is_departmental):

        user_type = common_helpers.get_dept_default_user_type(is_departmental)

        outcomes = self.filter(
            theme__baseplanpriority=base_plan_priority,
            user_type=user_type,
            is_departmental=is_departmental

        ).order_by('id')


        if school.school_type == 'Primary':
            return outcomes.exclude(secondary_only=True)
        elif school.school_type == 'Secondary':
            return outcomes.exclude(primary_only=True)
        else:
            return outcomes




class ThemeFeature(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    key_feature = models.CharField(max_length=200, default='', blank=True)
    exemplification_header = models.CharField(max_length=175, default='')
    user_type = models.CharField(max_length=10, default='Teacher')
    primary_only = models.BooleanField(default=False)
    secondary_only = models.BooleanField(default=False)
    is_departmental = models.BooleanField(default=False)

    objects = ThemeFeatureManager()

    def __str__(self):
        return self.exemplification_header



class FeatureExemplificationManager(models.Manager):

    def get_feature_exemplifications(self, theme_feature):
        return self.filter(
            theme_feature=theme_feature,
        ).order_by('id')

    def get_feature_exemplification(self, pk):
        return self.get(
            pk=pk,
        )

    def get_survey_feature_exemplifications(self, theme_feature, school_type):

        school_type = school_type.capitalize()

        if school_type == 'Primary':
            return self.filter(
                theme_feature=theme_feature,
                secondary_only=False
            ).order_by('id')

        elif school_type == 'Secondary':
            return self.filter(
                theme_feature=theme_feature,
                primary_only=False
            ).order_by('id')

        elif school_type == 'All':
            return self.filter(
                theme_feature=theme_feature
            ).order_by('id')

    def get_outcome_exemplifications(self, outcome):

        return self.filter(
            theme_feature=outcome
        ).order_by('id')


class FeatureExemplification(models.Model):
    theme_feature = models.ForeignKey(ThemeFeature, on_delete=models.CASCADE)
    exemplification = models.CharField(max_length=200)
    user_type = models.CharField(max_length=10, default='Teacher')
    primary_only = models.BooleanField(default=False)
    secondary_only = models.BooleanField(default=False)
    is_departmental = models.BooleanField(default=False)

    objects = FeatureExemplificationManager()

    def __str__(self):
        return self.exemplification




