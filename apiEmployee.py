from employeeApp import *

@app.route('/employees', methods=['POST','PUT','GET'])
def employees():
    if request.method == "POST":
        return addEmployee()
    if request.method == "PUT":
        return changeEmployee()
    if request.method == "GET":
        return employeesFiltered()
    
@app.route('/employee/<int:id>', methods=['GET','DELETE']) 
def employee(id):
    if request.method == "DELETE":
        return delete(id)
    if request.method == "GET":
        return getEmployees(id)

@app.route('/employees/plot1', methods=['GET'])
def plot_graph1():
    return plot1()

@app.route('/employees/plot2', methods=['GET'])
def plot_graph2():
    return plot2()

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=9007)   
