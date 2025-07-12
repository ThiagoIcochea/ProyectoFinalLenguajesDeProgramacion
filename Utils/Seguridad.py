import bcrypt

def hash_password(password):
   
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verificar_password(password, password_hasheado):
    if isinstance(password_hasheado, str):
        try:
            password_hasheado = password_hasheado.encode('utf-8') 
        except:
            print("El hash guardado no es válido")
            return False
    return bcrypt.checkpw(password.encode('utf-8'), password_hasheado)