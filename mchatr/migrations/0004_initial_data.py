from django.db import migrations, models

def create_initial_data(apps, schema_editor):
    Role = apps.get_model('mchatr', 'Role')
    School = apps.get_model('mchatr', 'School')

    # Create initial roles
    Role.objects.create(name='Professor')
    Role.objects.create(name='Responsável')

    # Create initial school
    School.objects.create(name='CEI City Jaragua IV', address='Rua José Galvez, 252 - Conj. City Jaragua, São Paulo - SP, 02998-270', email='ceicjaraguaiv@sme.prefeitura.sp.gov.br')
    School.objects.create(name='CEI Elohim Adonai', address='Rua Dr. Rafael de Araújo Ribeiro, 1185 - Jaraguá, São Paulo - SP, 05181-030', email='ceieadonai@sme.prefeitura.sp.gov.br')
    

class Migration(migrations.Migration):

    dependencies = [
        ('mchatr', '0003_role_school_userprofile'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]

