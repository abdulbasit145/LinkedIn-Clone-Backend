# Generated by Django 4.2.8 on 2023-12-26 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("cover_letter", models.TextField(blank=True, null=True)),
                (
                    "resume",
                    models.FileField(
                        blank=True, null=True, upload_to="JobApplications/Resumes/"
                    ),
                ),
                ("applied_at", models.DateTimeField(auto_now_add=True)),
                (
                    "applicant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="job_applications",
                        to="core.userprofile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Job Application",
                "verbose_name_plural": "Job Applications",
                "ordering": ["-applied_at"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name": "Tag",
                "verbose_name_plural": "Tags",
            },
        ),
        migrations.CreateModel(
            name="JobPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "applicants",
                    models.ManyToManyField(
                        related_name="applied_jobs",
                        through="job.JobApplication",
                        to="core.userprofile",
                    ),
                ),
                (
                    "recruiter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posted_jobs",
                        to="core.userprofile",
                    ),
                ),
                ("tags", models.ManyToManyField(related_name="jobs", to="job.tag")),
            ],
            options={
                "verbose_name": "Job Post",
                "verbose_name_plural": "Job Posts",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="job",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="applications",
                to="job.jobpost",
            ),
        ),
    ]
