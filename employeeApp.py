from flask import jsonify, request,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from datetime import datetime
from settings import *
import matplotlib.pyplot as plt
import io


db = SQLAlchemy(app) 
ma = Marshmallow(app)

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(80))
    Apellido = db.Column(db.String(80))
    DNI = db.Column(db.Integer)
    Fecha_Nacimiento = db.Column(db.Date)
    Fecha_Ingreso = db.Column(db.Date)
    def __init__(self,id,Nombre, Apellido,DNI,Fecha_Nacimiento,Fecha_Ingreso):
        self.id= id
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.DNI = DNI
        self.Fecha_Nacimiento = Fecha_Nacimiento
        self.Fecha_Ingreso = Fecha_Ingreso
    def json(self):
        return {"id" : self.id,
                "Nombre":self.Nombre,
                "Apellido":self.Apellido,
                "DNI":self.DNI,
                "Fecha_Nacimiento":self.Fecha_Nacimiento,
                "Fecha_Ingreso":self.Fecha_Ingreso}

db.create_all()

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','Nombre','Apellido','DNI','Fecha_Nacimiento','Fecha_Ingreso')

user_schema = UserSchema() 
users_schema = UserSchema(many=True)

#creo la funcion para calcular edad y antiguedad
def calculate(date):
    today = date.today()
    age = today.year - date.year - ((today.month, today.day) <(date.month, date.day))
    return age

#funcion que obtiene empleados por id
def getEmployees(id):
    try:
        query = jsonify([Employees.json(Employees.query.filter_by(id=id).first())])
    except:
        query = {'status': ('Empleado con Id = {0} no encontrado').format(id)}
    return query

#funcion que agrega empleados
def addEmployee():
    #print(request.json)
    for i in request.json:
        id = i['id']
        Nombre = i['Nombre']
        Apellido = i['Apellido']
        DNI = i['DNI']
        Fecha_Nacimiento = datetime.strptime(i['Fecha_Nacimiento'],"%d/%m/%Y")
        Fecha_Ingreso = datetime.strptime(i['Fecha_Ingreso'],'%d/%m/%Y')
        new_employee = Employees(id,Nombre,Apellido,DNI,Fecha_Nacimiento,Fecha_Ingreso) 
        db.session.commit()
        db.session.add(new_employee)
        db.session.commit()
    return {'status': 'Nuevo/s empleado/s añadido/s'}

#funcion que modifica valores de un empleado
def changeEmployee():
    Id = request.json['id']
    Nombre = request.json['Nombre']
    Apellido = request.json['Apellido']
    DNI = request.json['DNI']
    Fecha_Nacimiento = request.json['Fecha_Nacimiento']
    Fecha_Ingreso = request.json['Fecha_Ingreso']
    Employee_to_update = Employees.query.filter_by(id=Id).first()
    Employee_to_update.Id = Id
    Employee_to_update.Nombre = Nombre
    Employee_to_update.Apellido = Apellido
    Employee_to_update.DNI = DNI
    Employee_to_update.Fecha_Nacimiento = Fecha_Nacimiento
    Employee_to_update.Fecha_Ingreso = Fecha_Ingreso
    db.session.commit()
    return {'status': ('Empleado con Id = {0} modificado').format(Id)}

#funcion que elimina empleados por id
def delete(id):
    try:
        Employees.query.filter_by(id=id).delete()
        db.session.commit()
        query = {'status': ('Empleado con Id = {0} eliminado').format(id)}
    except:
        query = {'status': ('Empleado con Id = {0} no encontrado').format(id)}
    return query

#funcion que devuelve empleado filtrado por edad o por antiguedad
def employeesFiltered():
    #pregunta si en el request hay edad
    if 'edad' in  request.json:
        edad = request.json['edad']
        query = ([Employees.json(employee) for employee in Employees.query.all()])
        search = list(filter(None,list(map(lambda x : x if calculate(x['Fecha_Nacimiento']) == edad else None ,query))))
        if len(search)>0:
            response = jsonify(search)
        else:
            response = {'status': 'No se encontro informacion para el filtro de edad'}
    #pregunta si en el request hay antiguedad
    elif 'antiguedad' in  request.json:
        antiguedad = request.json['antiguedad']
        query = ([Employees.json(employee) for employee in Employees.query.all()])
        search = list(filter(None,list(map(lambda x : x if calculate(x['Fecha_Ingreso']) == antiguedad else None ,query))))
        if len(search)>0:
            response = jsonify(search)
        else:
            response = {'status': 'No se encontro informacion para el filtro de antiguedad'}
    else:
        response = {'status': 'No se encontro informacion para el filtro aplicado'}
    return response

#funcion que crea el grafico 1 
def grafico1(calculate,query):
    ages = list(map(lambda x :calculate(x['Fecha_Nacimiento']) ,query))
    plt.xlabel("edad")
    plt.ylabel("cantidad de empleados por edad")
    plt.title("edad de los empleados")
    bins = [20, 29, 30, 39, 40, 49, 50, 59, 60,69]
    plt.hist(ages,color='orange', bins = bins, edgecolor = 'black')
    #transformo la imagen en bytes
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image

#funcion que crea el grafico 2
def grafico2(calculate,query):
    ages = list(map(lambda x :calculate(x['Fecha_Nacimiento']) ,query))
    ant = list(map(lambda x :calculate(x['Fecha_Ingreso']) ,query))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(ages, ant)
    ax.set(title = "Relacion entre antiguedad y edad",
        xlabel = "edad",
        ylabel = "Antiguedad")
    #transformo la imagen en bytes
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image


#funcion que grafica y combierte los bytes en imagen para poder ser visualizada 
def plot1():
    query = ([Employees.json(employee) for employee in Employees.query.all()])
    bytes_obj = grafico1(calculate,query)
    
    return send_file(bytes_obj,
                     attachment_filename='plot1.png',
                     mimetype='image/png')

#funcion que grafica y combierte los bytes en imagen para poder ser visualizada 
def plot2():
    query = ([Employees.json(employee) for employee in Employees.query.all()])
    bytes_obj = grafico2(calculate,query)
    
    return send_file(bytes_obj,
                     attachment_filename='plot2.png',
                     mimetype='image/png')