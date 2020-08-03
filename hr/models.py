from django.db import models


class Cad_empresa(models.Model):
    nome = models.CharField(max_length=320)

    class Meta:
        managed = False
        db_table = 'cad_empresa'

    def __str__(self):
        return self.nome

class Cad_servico(models.Model):
    cad_empresa = models.ForeignKey(Cad_empresa, on_delete=models.CASCADE)
    nome = models.CharField(max_length=320)

    class Meta:
        managed = False
        db_table = 'cad_servico'

    def __str__(self):
        return self.nome

class Cad_veiculo(models.Model):
    nome = models.CharField(max_length=320)
    cad_servico = models.ForeignKey(Cad_servico, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'cad_veiculo'

    def __str__(self):
        return self.nome


class Person(models.Model):

    cad_empresa = models.ForeignKey(Cad_empresa, on_delete=models.SET_NULL, null=True)
    cad_servico = models.ForeignKey(Cad_servico, on_delete=models.SET_NULL, null=True)
    cad_veiculo = models.ForeignKey(Cad_veiculo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.cad_veiculo



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

    def __str__(self):
        return self.placa

