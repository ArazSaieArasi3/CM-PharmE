import RefOntoUML.parser.OntoUMLParser;
import RefOntoUML.Association;
import RefOntoUML.Property;
public class InspectReadOnly {
 public static void main(String[] args) throws Exception {
  OntoUMLParser p=new OntoUMLParser(args[0]);
  for(Association a:p.getAllInstances(Association.class))
   for(Property e:a.getMemberEnd())System.out.println(e.getName()+"|"+e.getType().getName()+"|"+e.isIsReadOnly());
 }
}
