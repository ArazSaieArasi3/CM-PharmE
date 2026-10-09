// Archived OLED parser smoke check: compiled against the pinned archived source.
import RefOntoUML.parser.OntoUMLParser;
import RefOntoUML.Association;
import RefOntoUML.Class;

public class ProbeParser {
    public static void main(String[] args) throws Exception {
        OntoUMLParser parser = new OntoUMLParser(args[0]);
        System.out.println("model=" + parser.getModelName()
          + " classes=" + parser.getAllInstances(Class.class).size()
          + " associations=" + parser.getAllInstances(Association.class).size());
    }
}
