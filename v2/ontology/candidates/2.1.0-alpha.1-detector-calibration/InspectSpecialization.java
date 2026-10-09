import RefOntoUML.parser.OntoUMLParser;
import RefOntoUML.Association;
import RefOntoUML.Property;
import java.util.ArrayList;
import java.util.Collections;
public class InspectSpecialization {
 public static void main(String[] args) throws Exception {
  OntoUMLParser p=new OntoUMLParser(args[0]);
  for(Association a:p.getAllInstances(Association.class))for(Property e:a.getMemberEnd()) {
   ArrayList<String> ss=new ArrayList<String>(),rr=new ArrayList<String>();
   for(Property q:e.getSubsettedProperty())ss.add(q.getName());
   for(Property q:e.getRedefinedProperty())rr.add(q.getName());
   Collections.sort(ss);Collections.sort(rr);
   System.out.println("END|"+e.getName()+"|"+e.getType().getName()+"|"+e.getLower()+"|"+e.getUpper()+"|"+String.join(",",ss)+"|"+String.join(",",rr));
  }
 }
}
