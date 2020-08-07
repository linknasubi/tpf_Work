from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class CadEmpresa(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cad_empresa'


class CadServico(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    nome = models.CharField(max_length=300, blank=True, null=True)
    interno = models.IntegerField(blank=True, null=True)
    cad_empresa_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cad_servico'


class CadVeiculo(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    cad_servico_id = models.IntegerField(blank=True, null=True)
    descricao = models.CharField(max_length=100, blank=True, null=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    lote = models.CharField(max_length=100, blank=True, null=True)
    servico = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cad_veiculo'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class HrCadEmpresa(models.Model):
    nome = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'hr_cad_empresa'


class HrCity(models.Model):
    nome = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'hr_city'


class TbLogExtracao(models.Model):
    date_start = models.CharField(max_length=100, blank=True, null=True)
    date_end = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    log = models.CharField(max_length=345, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_log_extracao'


class TbRastreioParada(models.Model):
    placa = models.CharField(max_length=100, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    segundos = models.IntegerField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    lote = models.CharField(max_length=45, blank=True, null=True)
    servico = models.CharField(max_length=45, blank=True, null=True)
    chamada = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_rastreio_parada'
