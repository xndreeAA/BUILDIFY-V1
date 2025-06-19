from app import db

class DetalleChasis(db.Model):
    __tablename__ = 'detalles_chasises'
    
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), primary_key=True)
    formato_soportado = db.Column(db.String(50))
    material = db.Column(db.String(50))
    alto_mm = db.Column(db.Integer)
    ancho_mm = db.Column(db.Integer)
    profundidad_mm = db.Column(db.Integer)
    peso_kg = db.Column(db.Numeric(5, 2))
    bahias_5_25 = db.Column(db.Integer, default=0)
    bahias_3_5 = db.Column(db.Integer, default=0)
    slots_expansion = db.Column(db.Integer, default=0)
    puertos_usb2 = db.Column(db.Integer, default=0)
    puertos_usb3 = db.Column(db.Integer, default=0)
    puerto_usb_c = db.Column(db.Integer, default=0)
    ventana_lateral = db.Column(db.Boolean, default=False)
    refrigeracion_incluye = db.Column(db.String(100))

    def __repr__(self):
        return f'<DetalleChasis {self.id_producto}>'

class DetalleFuentePoder(db.Model):
    __tablename__ = 'detalles_fuentes_poder'
    
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), primary_key=True)
    potencia_w = db.Column(db.Integer, nullable=False)
    certificacion_80plus = db.Column(db.Enum('Bronze', 'Silver', 'Gold', 'Platinum', 'Titanium', name='certificacion_enum'))
    modularidad = db.Column(db.Enum('No modular', 'Semi-modular', 'Full modular', name='modularidad_enum'))
    tipo_formato = db.Column(db.String(20))
    voltaje_12v_a = db.Column(db.Numeric(6, 2))
    num_conectores_24pin = db.Column(db.Integer, default=1)
    num_conectores_8pin = db.Column(db.Integer, default=0)
    num_sata = db.Column(db.Integer, default=0)
    num_molex = db.Column(db.Integer, default=0)
    protecciones_ip = db.Column(db.String(100))
    ventilador_mm = db.Column(db.Integer)
    ruido_max_db = db.Column(db.Numeric(5, 2))

    def __repr__(self):
        return f'<DetalleFuentePoder {self.id_producto}>'

class DetalleMemoriaRAM(db.Model):
    __tablename__ = 'detalles_memorias_ram'
    
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), primary_key=True)
    capacidad_gb = db.Column(db.Integer, nullable=False)
    tipo_ram = db.Column(db.Enum('DDR3', 'DDR4', 'DDR5', name='tipo_ram_enum'), nullable=False)
    velocidad_mhz = db.Column(db.Integer, nullable=False)
    num_modulos = db.Column(db.Integer, nullable=False)
    voltaje_v = db.Column(db.Numeric(3, 2))
    cl_latencia = db.Column(db.String(10))
    ecc = db.Column(db.Boolean, default=False)
    perfil_xmp = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<DetalleMemoriaRAM {self.id_producto}>'

class DetallePlacaBase(db.Model):
    __tablename__ = 'detalles_placas_base'
    
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), primary_key=True)
    socket = db.Column(db.String(20), nullable=False)
    chipset = db.Column(db.String(50), nullable=False)
    formato = db.Column(db.Enum('ATX', 'Micro-ATX', 'Mini-ITX', 'E-ATX', name='formato_enum'))
    num_slots_ram = db.Column(db.Integer, nullable=False)
    max_ram_gb = db.Column(db.Integer, nullable=False)
    pcie_x16_slots = db.Column(db.Integer, default=0)
    pcie_x8_slots = db.Column(db.Integer, default=0)
    pcie_x4_slots = db.Column(db.Integer, default=0)
    num_m2_slots = db.Column(db.Integer, default=0)
    num_sata_ports = db.Column(db.Integer, default=0)
    usb2_0_traseros = db.Column(db.Integer, default=0)
    usb3_0_traseros = db.Column(db.Integer, default=0)
    usb3_1_typeC_traseros = db.Column(db.Integer, default=0)
    lan_gbps = db.Column(db.Numeric(3, 1))
    wifi_integrado = db.Column(db.Boolean, default=False)
    bluetooth_integrado = db.Column(db.Boolean, default=False)
    fases_vrm = db.Column(db.Integer)
    audio_chipset = db.Column(db.String(50))

    def __repr__(self):
        return f'<DetallePlacaBase {self.id_producto}>'

class DetalleProcesador(db.Model):
    __tablename__ = 'detalles_procesadores'
    
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), primary_key=True)
    reloj_base_ghz = db.Column(db.Numeric(4, 2), nullable=False)
    reloj_boost_ghz = db.Column(db.Numeric(4, 2))
    num_nucleos = db.Column(db.Integer, nullable=False)
    num_hilos = db.Column(db.Integer, nullable=False)
    tdp_w = db.Column(db.Integer)
    socket = db.Column(db.String(20))
    litografia_nm = db.Column(db.Integer)
    cache_l2_mb = db.Column(db.Numeric(5, 2))
    cache_l3_mb = db.Column(db.Numeric(6, 2))
    gpu_integrado = db.Column(db.String(100))

    def __repr__(self):
        return f'<DetalleProcesador {self.id_producto}>'

class DetalleRefrigeracion(db.Model):
    __tablename__ = 'detalles_refrigeraciones'
    
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), primary_key=True)
    tipo_refrigeracion = db.Column(db.Enum('Aire', 'Líquida', name='tipo_refrigeracion_enum'), nullable=False)
    altura_mm = db.Column(db.Integer)
    ventilador_mm = db.Column(db.Integer)
    flujo_aire_cfm = db.Column(db.Numeric(6, 2))
    nivel_ruido_db = db.Column(db.Numeric(5, 2))
    socket_compatibles = db.Column(db.String(100))
    radiador_mm = db.Column(db.String(20))
    bombas_rpm = db.Column(db.Integer)
    conductos_material = db.Column(db.String(50))
    peso_kg = db.Column(db.Numeric(5, 2))

    def __repr__(self):
        return f'<DetalleRefrigeracion {self.id_producto}>'

class DetalleTarjetaGrafica(db.Model):
    __tablename__ = 'detalles_tarjetas_graficas'
    
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), primary_key=True)
    chipset = db.Column(db.String(50), nullable=False)
    memoria_gb = db.Column(db.Integer, nullable=False)
    tipo_memoria = db.Column(db.String(20))
    bus_memoria_bits = db.Column(db.Integer)
    reloj_base_ghz = db.Column(db.Numeric(5, 2))
    reloj_boost_ghz = db.Column(db.Numeric(5, 2))
    tdp_w = db.Column(db.Integer)
    pcie_version = db.Column(db.String(10))
    cuda_cores = db.Column(db.Integer)
    long_mm = db.Column(db.Integer)
    altura_mm = db.Column(db.Integer)
    espesor_slots = db.Column(db.Numeric(3, 1))
    conector_6pin = db.Column(db.Integer, default=0)
    conector_8pin = db.Column(db.Integer, default=0)
    sli_xfire_soporte = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<DetalleTarjetaGrafica {self.id_producto}>'