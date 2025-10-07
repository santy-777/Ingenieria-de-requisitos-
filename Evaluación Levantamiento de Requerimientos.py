import csv
import os


class ContactNode:
    """Nodo de lista doblemente enlazada que representa un contacto."""
    def __init__(self, nombre: str, telefono: str, correo: str, cargo: str):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.cargo = cargo
        self.next = None
        self.prev = None


class ContactList:
    """Lista doblemente enlazada para manejar los contactos."""
    def __init__(self):
        self.head = None
        self.tail = None
        self.load_contacts()

    def load_contacts(self):
        """Carga contactos desde el archivo CSV si existe."""
        if os.path.exists("contactos.csv"):
            with open("contactos.csv", newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.add_contact(row['nombre'], row['telefono'], row['correo'], row['cargo'], save=False)

    def save_contacts(self):
        """Guarda todos los contactos en el archivo CSV."""
        with open("contactos.csv", "w", newline='', encoding='utf-8') as file:
            fieldnames = ["nombre", "telefono", "correo", "cargo"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            temp = self.head
            while temp:
                writer.writerow({
                    "nombre": temp.nombre,
                    "telefono": temp.telefono,
                    "correo": temp.correo,
                    "cargo": temp.cargo
                })
                temp = temp.next

    def add_contact(self, nombre: str, telefono: str, correo: str, cargo: str, save=True):
        """Agrega un contacto nuevo validando que el correo no esté repetido."""
        if self.find_by_email(correo):
            print("⚠️ Ya existe un contacto con ese correo.")
            return False

        new_node = ContactNode(nombre, telefono, correo, cargo)

        if not self.head:
            self.head = self.tail = new_node
        else:
            temp = self.head
            while temp and temp.nombre.lower() < nombre.lower():
                temp = temp.next
            if not temp:
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node
            elif temp == self.head:
                new_node.next = self.head
                self.head.prev = new_node
                self.head = new_node
            else:
                prev_node = temp.prev
                new_node.next = temp
                new_node.prev = prev_node
                prev_node.next = new_node
                temp.prev = new_node

        if save:
            self.save_contacts()
        print("✅ Contacto agregado correctamente.")
        return True

    def find_by_name(self, nombre: str):
        """Busca un contacto por nombre."""
        temp = self.head
        while temp:
            if temp.nombre.lower() == nombre.lower():
                return temp
            temp = temp.next
        return None

    def find_by_email(self, correo: str):
        """Busca un contacto por correo."""
        temp = self.head
        while temp:
            if temp.correo.lower() == correo.lower():
                return temp
            temp = temp.next
        return None

    def list_contacts(self):
        """Devuelve una lista con todos los contactos registrados."""
        contacts = []
        temp = self.head
        while temp:
            contacts.append((temp.nombre, temp.telefono, temp.correo, temp.cargo))
            temp = temp.next
        return contacts

    def delete_contact(self, correo: str):
        """Elimina un contacto existente según su correo."""
        temp = self.find_by_email(correo)
        if not temp:
            print("⚠️ No se encontró el contacto.")
            return False

        if temp.prev:
            temp.prev.next = temp.next
        else:
            self.head = temp.next

        if temp.next:
            temp.next.prev = temp.prev
        else:
            self.tail = temp.prev

        self.save_contacts()
        print("🗑️ Contacto eliminado correctamente.")
        return True


def wait_return():
    input("\nPresione cualquier tecla para volver al menú: ")


def menu():
    contact_list = ContactList()

    while True:
        print("\n📇 Menú del Directorio ConnectMe 📇")
        print("1. Registrar nuevo contacto")
        print("2. Buscar contacto por nombre")
        print("3. Buscar contacto por correo")
        print("4. Listar todos los contactos")
        print("5. Eliminar contacto")
        print("6. Salir")

        choice = input("Seleccione una opción: ")

        if choice == "1":
            nombre = input("Ingrese el nombre: ")
            telefono = input("Ingrese el número de teléfono: ")
            correo = input("Ingrese el correo electrónico: ")
            cargo = input("Ingrese el cargo: ")
            contact_list.add_contact(nombre, telefono, correo, cargo)
            wait_return()

        elif choice == "2":
            nombre = input("Ingrese el nombre del contacto: ")
            contact = contact_list.find_by_name(nombre)
            if contact:
                print(f"\n📞 Nombre: {contact.nombre}\n📱 Teléfono: {contact.telefono}\n📧 Correo: {contact.correo}\n💼 Cargo: {contact.cargo}")
            else:
                print("⚠️ Contacto no encontrado.")
            wait_return()

        elif choice == "3":
            correo = input("Ingrese el correo del contacto: ")
            contact = contact_list.find_by_email(correo)
            if contact:
                print(f"\n📞 Nombre: {contact.nombre}\n📱 Teléfono: {contact.telefono}\n📧 Correo: {contact.correo}\n💼 Cargo: {contact.cargo}")
            else:
                print("⚠️ Contacto no encontrado.")
            wait_return()

        elif choice == "4":
            contacts = contact_list.list_contacts()
            if contacts:
                print("\n📋 Contactos registrados:")
                for c in contacts:
                    print(f"• {c[0]} | {c[1]} | {c[2]} | {c[3]}")
            else:
                print("⚠️ No hay contactos registrados.")
            wait_return()

        elif choice == "5":
            correo = input("Ingrese el correo del contacto a eliminar: ")
            contact_list.delete_contact(correo)
            wait_return()

        elif choice == "6":
            print("👋 Saliendo del directorio ConnectMe...")
            break

        else:
            print("⚠️ Opción inválida.")
            wait_return()


if __name__ == "__main__":
    menu()

