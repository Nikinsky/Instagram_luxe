# Generated by Django 5.1.4 on 2024-12-22 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0004_rename_image_postvideo_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='instagram.comment'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='commentlike',
            unique_together={('user', 'like')},
        ),
        migrations.AlterUniqueTogether(
            name='postlike',
            unique_together={('user', 'like')},
        ),
    ]
