import RefOntoUML.parser.OntoUMLParser;
import RefOntoUML.Association;
import RefOntoUML.DataType;
import RefOntoUML.Generalization;
import RefOntoUML.GeneralizationSet;
import RefOntoUML.Property;
import java.util.ArrayList;
import java.util.Collections;
public class InspectLegacy {
 public static void main(String[] args) throws Exception {
  OntoUMLParser p=new OntoUMLParser(args[0]);
  for(RefOntoUML.Class c:p.getAllInstances(RefOntoUML.Class.class))
   System.out.println("CLASS|"+c.getName()+"|"+c.eClass().getName()+"|"+c.isIsAbstract());
  for(DataType c:p.getAllInstances(DataType.class))
   System.out.println("CLASS|"+c.getName()+"|"+c.eClass().getName()+"|"+c.isIsAbstract());
  for(Association a:p.getAllInstances(Association.class)) {
   System.out.println("REL|"+a.getName()+"|"+a.eClass().getName());
   int i=0;
   for(Property e:a.getMemberEnd()) {
    ArrayList<String> subs=new ArrayList<String>();for(Property q:e.getSubsettedProperty())subs.add(q.getName());Collections.sort(subs);
    System.out.println("END|"+a.getName()+"|"+(i++)+"|"+e.getName()+"|"+e.getType().getName()+"|"+e.getLower()+"|"+e.getUpper()+"|"+e.getAggregation().getLiteral()+"|"+String.join(",",subs));
   }
  }
  for(Generalization g:p.getAllInstances(Generalization.class))
   System.out.println("GEN|"+g.getSpecific().getName()+"|"+g.getGeneral().getName());
  for(GeneralizationSet gs:p.getAllInstances(GeneralizationSet.class)) {
   ArrayList<String> gens=new ArrayList<String>();for(Generalization g:gs.getGeneralization())gens.add(g.getSpecific().getName()+">"+g.getGeneral().getName());Collections.sort(gens);
   System.out.println("SET|"+gs.getName()+"|"+gs.isIsDisjoint()+"|"+gs.isIsCovering()+"|"+String.join(",",gens));
  }
 }
}
