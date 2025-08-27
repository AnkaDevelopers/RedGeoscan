import win32com.client

olFolderInbox = 6

outlook = win32com.client.Dispatch("Outlook.Application")
ns = outlook.GetNamespace("MAPI")

print("=== LISTA DE ALMACENES (STORES) ===")
for i in range(1, ns.Stores.Count + 1):
    store = ns.Stores.Item(i)
    print(f"\n[{i}] Store: {store.DisplayName}")
    try:
        inbox = store.GetDefaultFolder(olFolderInbox)
        print(f"   - Inbox path: {inbox.FolderPath}")
        print(f"   - Inbox items: {inbox.Items.Count}")
    except Exception as e:
        print(f"   - No pude leer Inbox en este store: {e}")

print("\n=== LISTA DE CUENTAS (SESSIONS/FOLDERS TOP-LEVEL) ===")
for i in range(1, ns.Folders.Count + 1):
    root = ns.Folders.Item(i)
    print(f"\n[{i}] Root: {root.Name}")
    try:
        inbox = root.Folders("Bandeja de entrada")  # nombre en español
        print(f"   - {inbox.FolderPath} -> {inbox.Items.Count} items")
    except Exception as e:
        try:
            inbox = root.Folders("Inbox")  # por si viene en inglés
            print(f"   - {inbox.FolderPath} -> {inbox.Items.Count} items")
        except Exception as e2:
            print("   - No encontré 'Bandeja de entrada' ni 'Inbox' en este root.")
