# Μετατροπέας Φωτο / ImageCropper

Βασική χρήση:

1) Διαβάζει αρχεία από φάκελο Source Files
2) Μετατρέπει τις φωτογραφίες σε 740x740 pixels
3) Τις αποθηκεύει στον φάκελο Output Files
4) Εάν αντιμετωπίσει πρόβλημα, γράφει το όνομα του προβληματικού αρχείου στο έγγραφο errorlog.txt

Η εφαρμογή φτιάχνει μόνη της όλα τα απαραίτητα αρχεία για την εξαγωγή των εικόνων, οπότε ο φάκελος
Output Files μπορεί να σβηστεί ολόκληρος.

Πρέπει όμως πάντα να υπάρχει φάκελος με την ονομασία "Source Files" εκτός αν έχει ρυθμιστεί διαφορετικά
στο config.json

----------------------------

Προχωρημένη χρήση:

Η δημιουργία ενώς αρχείου config.json αλλάζει την συμπεριφορά του προγράμματος

πεδία με παραδείγματα και επεξηγήσεις:

{
    "inputfile":"Source Files", // Όνομα του φακέλου όπου εισάγωνται οι εικόνες
    "outputfile":"Output Files", // Όνομα του φακέλου που εξάγωνται οι εικόνες
    "errorlog":"errorlog.txt", // Όνομα του αρχείου που καταγράφει τα σφάλματα κατα την λειτουργία της εφαρμογής
    "dimensions":[[740, 740]] // Λίστα διαστάσεων, [[πλάτος1, ύψος1], [πλάτος2, ύψος2], ....]
}

To config.json μπορεί να απενεργοποιηθεί με το πεδίο "mode":"ignore"

----------------------------

Ως module:

Ο κώδικας μπορεί να χρησιμοποιηθεί από άλλες εφαρμογές ως import και τρέχοντας την main() function
Είναι απαραίτητο να περαστεί ένα Config object με το όνομα του φακέλου που περιέχει τις εισαγώμενες
εικόνες (inputfile / default: Source File ) ως argument στην main().

Παράδειγμα χρήσης:

import ImageCropper as IC
config = IC.Config(inputfile = "Downloaded Images")
IC.main(config=config)

----------------------------

Multithreading: 

Το πρόγραμμα χρησιμοποιεί τα μισά από τα threads του υπολογιστή. Αυτό μπορεί να αλλάξει προσθέτοντας
το πεδίο "threads":integer στο config.json

----------------------------


Devnotes:

py2exe makes the application frozen. For multithreaded applications, this requires to import
the free_support function of the multiprocessing module and run it under the __name__ check

Additionally, by making it an exe, it doesn't have a __file__ attribute anymore. The relevant
code looks like this


if hasattr(sys, "frozen"):
    root_dir = rootdir = os.path.abspath(os.path.dirname(sys.executable))
else:
    root_dir = os.path.abspath(os.path.dirname(__file__))
