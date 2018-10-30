import psycopg2
from flask import Flask, render_template, request, url_for



app = Flask(__name__)
def getCon():

    connStr=("dbname='ticket_data' user='postgres' password='password'")

    conn = psycopg2.connect(connStr)

    return conn

@app.route('/')
def home():
    return render_template('index.html')

#Function for creating a new Customer

@app.route('/addCustomer', methods =['POST'])
def addCustomer():
     try:
         conn = None
         CustomerID = int(request.form['CustomerID'])
         Name = request.form['Name']
         Email = request.form['Email']

         conn = getCon()
         cur = conn.cursor()
         cur.execute('SET search_path to public')

         cur.execute('INSERT INTO Customer VALUES (%s, %s, %s)', [CustomerID, Name, Email])
         conn.commit()
         return render_template('index.html', msg = 'Customer Added')

     except Exception as e:
         return render_template('index.html', msg = 'Unable to add customer', err=e)

     finally:
         if conn:
             conn.close()

''''
@app.route('/displayCustomer', methods = ['GET'])
def displayCustomer():
    try:
        CustomerID = int(request.form['CustomerID'])

        conn = None
        conn = getCon()
        cur = conn.cursor()
        cur.execute('SET search_path to public')

        cur.execute('SELECT distinct CustomerID, Name, Email From Customer WHERE CustomerID = %s' [CustomerID])

        rows = cur.fetchall()
        if rows:
            return render_template('customer.html', rows = rows)
        else:
            return render_template('index.html', msg2 = 'Nothing here')

    except Exception as e:
        return render_template('index.html', msg2 = 'No data found', err2 = e)

    finally:
        if conn:
            conn.close()'''


@app.route('/addTicket', methods =['GET', 'POST'])
def addTicket():
     try:
         conn = None
         TicketID = int(request.form['TicketID'])
         Problem = request.form['Problem']
         Status = request.form['Status']
         Priority = int(request.form['Priority'])
         LoggedTime = request.form['LoggedTime']
         CustomerID = int(request.form['CustomerID'])
         ProductID = int(request.form['ProductID'])


         conn = getCon()
         cur = conn.cursor()
         cur.execute('SET search_path to public')

         cur.execute('INSERT INTO Ticket VALUES (%s, %s, %s, %s, %s, %s, %s)', [TicketID, Problem, Status, Priority, LoggedTime, CustomerID, ProductID])
         conn.commit()
         return render_template('index.html', msg1 = 'Ticket Added')

     except Exception as e:
         return render_template('index.html', msg1 = 'Unable to add Ticket', err1=e)

     finally:
         if conn:
             conn.close()


@app.route('/displayTicket', methods = ['GET'])
def displayTicket():
    try:
        conn = None
        conn = getCon()
        cur = conn.cursor()
        cur.execute('SET search_path to public')

        cur.execute('SELECT * FROM Ticket')

        rows = cur.fetchall()
        if rows:
            return render_template('ticket.html', rows = rows)
        else:
            return render_template('index.html', msg2 = 'No Tickets here')

    except Exception as e:
        return render_template('index.html', msg2 = "No Tickets here", err2 = e)

    finally:
        if conn:
            conn.close()

@app.route('/updateTicket', methods = ['POST'])
def updateTicket():
    try:

        Conn = None
        TicketUpdateID = int(request.form['TicketUpdateID'])
        Message = request.form['Message']
        UpdateTime = request.form['UpdateTime']
        TicketID = int(request.form['TicketID'])
        StaffID = int(request.form['StaffID'])

        conn = getCon()
        cur = conn.cursor()
        cur.execute('SET search_path to public')

        cur.execute('INSERT INTO TicketUpdate VALUES (%s, %s, %s, %s, %s)' [TicketUpdateID, Message, UpdateTime, TicketID, StaffID])
        conn.commit()
        return render_template('index.html', msg3 = 'Ticket has been updated')

    except Exception as e:
        return render_template('index.html', msg3 = 'Unable to update Ticket', err3 = e)
    
    finally:
        if conn: 
            conn.close()


@app.route('/listOpen', methods = ['GET'])
def listOpen():
    try:

        conn = None
        conn = getCon()
        cur = conn.cursor()
        cur.execute('SET search_path to public')

        cur.execute("SELECT distinct ticket.ticketid, ticket.status, ticket.loggedtime FROM ticket RIGHT JOIN TicketUpdate ON Ticket.TicketID=TicketUpdate.TicketID WHERE TICKET.status = 'Open'")

        rows = cur.fetchall()
        if rows:
            return render_template('ticket.html', rows = rows)
        else:
            return render_template('index.html', msg4 = 'No Tickets here')

    except Exception as e:
        return render_template('index.html', msg4 = 'No Tickets here', err4 = e)

    finally:
        if conn:
            conn.close()


@app.route('/changeStatus', methods = ['POST'])
def changeStatus():
    try:
        conn = None
        Status = request.form['Status']
        TicketID = int(request.form['TicketID'])

        conn = getCon()
        cur = conn.cursor()
        cur.execute('SET search_path to public')

        cur.execute('UPDATE Ticket SET Status = (%s) WHERE TicketID = (%s)', [Status, TicketID])
        conn.commit()
        return render_template('index.html', msg5='Support Ticket updated')

    except Exception as e:
        return render_template('index.html', msg5='Unable to update support ticket', err5=e)

    finally:
        if conn:
            conn.close()

@app.route('/orgProblem', methods = ['GET', 'POST '])
def orgProblem():
    try:
        conn = None
        Ticket.TicketID = request.form['TicketID']

        conn = getCon()
        cur = conn.cursor()
        cur.execute('SET search_path to public')

        cur.execute('SELECT Distinct Ticket.TicketID, Ticket.LoggedTime, Customer.Name FROM Ticket, TicketUpdate, Customer WHERE TicketUpdate.TicketUpdateID = Ticket.TicketID AND Ticket.CustomerID = Customer.CustomerID AND  Ticket.TicketID = (%s) ORDER BY TicketUpdate.UpdateTime ASC' /
                    [Ticket.TicketID]
                    )
        conn.commit()
        return render_template('index.html', msg6='Support Ticket updated')

    except Exception as e:
        return render_template('index.html', msg6='Unable to list Original Problem', err6=e)

    finally:
        if conn:
            conn.close()


@app.route('/listClose', methods = ['GET'])
def listClose():
    try:
        conn = None
        conn = getCon()
        cur = conn.cursor()
        cur.execute('SET search_path to public')

        cur.execute("SELECT DISTINCT Ticket.Status, Ticket.Problem, TicketUpdate.UpdateTime, Ticket.LoggedTime, TicketUpdate.UpdateTime, COUNT(TicketUpdate.TicketUpdateID) AS Staff_Updates, MAX(TicketUpdate.UpdateTime::timestamp) - Ticket.LoggedTime::timestamp AS Difference FROM Ticket, TicketUpdate WHERE Ticket.Status = 'Closed' AND Ticket.TicketID = TicketUpdate.TicketID GROUP BY Problem, UpdateTime, LoggedTime, Status")  #SQL statements go here

        rows = cur.fetchall()
        if rows:
            return render_template('ticket.html', rows=rows)
        else:
            return render_template('index.html', msg7='No Tickets here')

    except Exception as e:
        return render_template('index.html', msg7='Unable to comoplete request', err7=e)

    finally:
        if conn:
            conn.close()


@app.route('/deleteCustomer', methods = ['GET', 'POST'])
def deleteCustomer():
    try:
        conn = None
        CustomerID = int(request.form['CustomerID'])

        conn = getCon()
        cur = conn.cursor()
        cur.execute('SET search_path to public')

        cur.execute('DELETE FROM Customer WHERE CustomerID = (%s)', [CustomerID]) #sql Statement goes here
        conn.commit()
        return render_template('index.html', msg8='Customer Deleted')

    except Exception as e:
        return render_template('index.html', msg8='Unable to delete customer', err8=e)

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
 app.run(debug = True)
