# Generated by Django 4.2.5 on 2023-11-05 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attandance', '0007_alter_project_breadth_alter_project_length_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoryName', models.CharField(max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='contractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attandance.contractor'),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='labor_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attandance.labortypes'),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attandance.project'),
        ),
        migrations.AlterField(
            model_name='overtimerecord',
            name='contractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attandance.contractor'),
        ),
        migrations.AlterField(
            model_name='overtimerecord',
            name='labor_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attandance.labortypes'),
        ),
        migrations.AlterField(
            model_name='overtimerecord',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attandance.project'),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Materialname', models.CharField(max_length=500)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attandance.materialcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Indent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.DecimalField(decimal_places=2, default='0', max_digits=10)),
                ('Quantity_order_status', models.BooleanField()),
                ('Quantity_Recieved_status', models.BooleanField()),
                ('CategoryName', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attandance.materialcategory')),
                ('Material', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attandance.material')),
                ('Project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attandance.project')),
            ],
        ),
    ]