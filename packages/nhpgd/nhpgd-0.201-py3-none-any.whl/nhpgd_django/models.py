from django.db import models
import logging
logger = logging.getLogger(__name__)


class NomencladorHPGD(models.Model):
    """ cada uno de los códigos del nomenclador 
        de JHospitales Públicos de Gestión Descentralizada
        del Anexo II
        https://github.com/cluster311/Anexo2
        """
    codigo = models.CharField(max_length=20)
    # como los códigos se repiten uso el de la librería para diferenciar
    uid = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=190)
    arancel = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.codigo} {self.descripcion}'
    
    @classmethod
    def start_db(cls):
        logger.info('Comenzando importacion de Nomenclador HPGD')
        from nhpgd.nomenclador import Nomenclador
        nom = Nomenclador()
        # fields ['codigo', 'descripcion', 'arancel', 'observaciones']
        for c, elem in nom.tree.items():
            code = elem[codigo]
            logger.info(f'{c} Imporatando código {code}')
            n, created = NomencladorHPGD.objects.get_or_create(uid=c, code=code)
            n.descripcion = elem['descripcion']
            n.arancel = float(elem['arancel'])
            n.observaciones = elem['observaciones']
            n.save()
        
        return True

