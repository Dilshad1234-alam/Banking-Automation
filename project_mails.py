import gmail
# email='xxxxxxxx@gmail.com'        # mention your gmail id
# app_pass='xxxxxxxx'               # mention app password

def send_mail_for_openacn(to_mail,uacno,uname,upass,udate):
    
        con=gmail.GMail('dmd68699@gmail.com','xtfl quzt cthi dmdd')
        sub='Account opend with ABC Bank'
        body=f"""DEAR {uname},
        your account has opened successfully with ABC Bank and details are
    ACN = {uacno}
    pass = {upass}
    open date = {udate}

    kindly change your password you login first time
    Thanks
    ABC Bank
    Noida
    """
        msg=gmail.Message(to=to_mail,subject=sub,text=body)
        con.send(msg)                                      

def send_otp(to_mail,uname,uotp):

    con=gmail.GMail('dmd68699@gmail.com','xtfl quzt cthi dmdd')
    sub='OTP for password recovery'
    body=f"""DEAR {uname},
        your OTP to get password = {uotp}
    
    kindly verify this otp to application 
    Thanks
    ABC Bank
    Noida
    """

    msg=gmail.Message(to=to_mail,subject=sub,text=body)
    con.send(msg)
                                                                                                                                                                              
       