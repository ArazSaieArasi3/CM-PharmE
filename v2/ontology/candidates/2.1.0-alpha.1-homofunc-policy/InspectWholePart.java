import RefOntoUML.componentOf;
import RefOntoUML.Property;
import RefOntoUML.parser.OntoUMLParser;
/** Checks the unchanged official parser's aggregation-bound endpoint roles. */
public class InspectWholePart {
    public static void main(String[] args) throws Exception {
        OntoUMLParser p = new OntoUMLParser(args[0]);
        for (componentOf m : p.getAllInstances(componentOf.class)) {
            Property w = OntoUMLParser.getWholeEnd(m);
            Property t = OntoUMLParser.getPartEnd(m);
            System.out.println("ROLES|"+m.getName()+"|"+w.getName()+"|"+w.getType().getName()+"|"+t.getName()+"|"+t.getType().getName());
        }
    }
}
