// A narrow archived-OLED BinOver sensitivity check on a converted toy XMI.
import RefOntoUML.parser.OntoUMLParser;
import RefOntoUML.Association;
import RefOntoUML.Class;
import RefOntoUML.Characterization;
import RefOntoUML.Property;
import br.ufes.inf.nemo.antipattern.binover.BinOverAntipattern;

public class ProbePatterns {
    public static void main(String[] args) throws Exception {
        OntoUMLParser parser = new OntoUMLParser(args[0]);
        int classes = parser.getAllInstances(Class.class).size();
        int associations = parser.getAllInstances(Association.class).size();
        int binOver = new BinOverAntipattern(parser).identify().size();
        System.out.println("model=" + parser.getModelName()
          + " classes=" + classes + " associations=" + associations
          + " characterizations=" + parser.getAllInstances(Characterization.class).size()
          + " BinOver=" + binOver);
        for (Association relation : parser.getAllInstances(Association.class)) {
            System.out.println("relation=" + relation.getName()
              + " kind=" + relation.getClass().getSimpleName()
              + " ends=" + relation.getMemberEnd().size());
            for (Property end : relation.getMemberEnd()) {
                System.out.println("end=" + end.getName() + " type=" + end.getType().getName()
                  + " card=" + end.getLower() + ".." + end.getUpper());
            }
        }
    }
}
