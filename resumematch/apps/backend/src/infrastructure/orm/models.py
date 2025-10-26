from django.db import models


class CandidateModel(models.Model):
    full_name = models.CharField(max_length=255)
    contact_email = models.EmailField(null=True, blank=True)
    location = models.CharField(max_length=255)
    years_exp = models.IntegerField()
    skills_json = models.JSONField(default=list)
    resume_file_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class VacancyModel(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    skills_req_json = models.JSONField(default=list)
    jd_file_id = models.CharField(max_length=255, null=True, blank=True)
    jd_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class LabelModel(models.Model):
    vacancy = models.ForeignKey(VacancyModel, on_delete=models.CASCADE)
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    label = models.CharField(max_length=10)
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)