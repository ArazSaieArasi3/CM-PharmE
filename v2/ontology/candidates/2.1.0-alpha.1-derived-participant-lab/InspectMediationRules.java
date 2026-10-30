import RefOntoUML.parser.OntoUMLParser;
import RefOntoUML.Mediation;
import RefOntoUML.util.RefOntoUMLValidator;
import java.util.HashMap;
public class InspectMediationRules {
 public static void main(String[] args) throws Exception {
  OntoUMLParser p=new OntoUMLParser(args[0]);
  RefOntoUMLValidator v=RefOntoUMLValidator.INSTANCE;
  for(Mediation m:p.getAllInstances(Mediation.class)) {
   System.out.println("RULE|"+m.getName()+"|source-lower|"+v.validateDependencyRelationship_DependencyRelationshipConstraint1(m,null,new HashMap<Object,Object>()));
   System.out.println("RULE|"+m.getName()+"|target-readonly|"+v.validateDependencyRelationship_DependencyRelationshipConstraint2(m,null,new HashMap<Object,Object>()));
   System.out.println("RULE|"+m.getName()+"|target-lower|"+v.validateMediation_MediationConstraint2(m,null,new HashMap<Object,Object>()));
  }
 }
}
