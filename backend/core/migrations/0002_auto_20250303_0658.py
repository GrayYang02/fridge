from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),  # 确保这里填写上一个迁移文件的名称
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='food',
            field=models.TextField(),
        ),
    ]
