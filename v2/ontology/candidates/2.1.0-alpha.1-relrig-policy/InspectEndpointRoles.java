import RefOntoUML.Mediation;
import RefOntoUML.Property;
import RefOntoUML.parser.OntoUMLParser;
/** Inspects actual pinned parser end-role resolution, independently of Python. */
public class InspectEndpointRoles {
    public static void main(String[] args) throws Exception {
        OntoUMLParser p = new OntoUMLParser(args[0]);
        for (Mediation m : p.getAllInstances(Mediation.class)) {
            Property r = OntoUMLParser.getRelatorEnd(m);
            Property t = OntoUMLParser.getMediatedEnd(m);
            System.out.println("ROLES|" + m.getName() + "|" + r.getName() + "|" + r.getType().getName() + "|" + r.isIsReadOnly() + "|" + t.getName() + "|" + t.getType().getName() + "|" + t.isIsReadOnly());
        }
    }
}
