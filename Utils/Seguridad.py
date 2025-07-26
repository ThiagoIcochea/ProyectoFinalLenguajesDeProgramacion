# Importa la biblioteca bcrypt, que se utiliza para cifrar y verificar contraseñas de forma segura.
import bcrypt

# Función que recibe una contraseña en texto plano y devuelve su versión hasheada (cifrada)
def hash_password(password):
    # Codifica la contraseña en formato UTF-8 y genera un hash seguro con un "salt" (valor aleatorio)
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Función que verifica si una contraseña ingresada coincide con un hash previamente guardado
def verificar_password(password, password_hasheado):
    # Si el hash guardado es una cadena (str), se convierte a bytes
    if isinstance(password_hasheado, str):
        try:
            password_hasheado = password_hasheado.encode('utf-8')  # Codifica el hash a bytes
        except:
            # Si ocurre un error en la conversión, se muestra un mensaje y se retorna False
            print("El hash guardado no es válido")
            return False

    # Verifica si la contraseña ingresada coincide con el hash (ambos en formato bytes)
    return bcrypt.checkpw(password.encode('utf-8'), password_hasheado)
