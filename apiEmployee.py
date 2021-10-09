from employeeApp import *

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    return getEmployees(id)

@app.route('/employees', methods=['POST'])
def add_employee():
    return addEmployee()

@app.route('/employees', methods=['PUT'])
def put():
    return changeEmployee()

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    return delete(id)

@app.route('/employees', methods=['GET'])
def employees_Filtered():
    return employeesFiltered()

@app.route('/employees/plot1', methods=['GET'])
def plot_graph1():
    return plot1()

@app.route('/employees/plot2', methods=['GET'])
def plot_graph2():
    return plot2()

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=9007)   
