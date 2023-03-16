from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://miusuario:micontraseña@localhost/delivery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    entregas = db.relationship('Entrega', backref='cliente', lazy=True)

class Entrega(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    numero_de_boleta = db.Column(db.String(255), nullable=False)
    entregado = db.Column(db.Boolean, nullable=False, default=False)

@app.route('/clientes', methods=['POST'])
def agregar_cliente():
    nombre = request.json['nombre']
    direccion = request.json['direccion']
    nuevo_cliente = Cliente(nombre=nombre, direccion=direccion)
    db.session.add(nuevo_cliente)
    db.session.commit()
    return jsonify({"mensaje": "Cliente agregado exitosamente"}), 201

@app.route('/entregas', methods=['POST'])
def agregar_entrega():
    cliente_id = request.json['cliente_id']
    numero_de_boleta = request.json['numero_de_boleta']
    nueva_entrega = Entrega(cliente_id=cliente_id, numero_de_boleta=numero_de_boleta)
    db.session.add(nueva_entrega)
    db.session.commit()
    return jsonify({"mensaje": "Entrega agregada exitosamente"}), 201

@app.route('/entregas', methods=['GET'])
def obtener_entregas():
    entregas = Entrega.query.all()
    resultado = [
        {
            "id": entrega.id,
            "cliente_id": entrega.cliente_id,
            "numero_de_boleta": entrega.numero_de_boleta,
            "entregado": entrega.entregado
        }
        for entrega in entregas
    ]
    return jsonify(resultado)

@app.route('/entregas/<int:id>', methods=['PUT'])
def actualizar_entrega(id):
    entrega = Entrega.query.get_or_404(id)
    entrega.entregado = request.json['entregado']
    db.session.commit()
    return jsonify({"mensaje": "Entrega actualizada exitosamente"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
