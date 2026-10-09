import RefOntoUML.parser.OntoUMLParser;
import RefOntoUML.Class;
import RefOntoUML.Association;
import br.ufes.inf.nemo.antipattern.Antipattern;
public class RuntimeCatalogue {
 public static void main(String[] args) throws Exception {
  OntoUMLParser p=new OntoUMLParser(args[1]);
  Antipattern detector;
  switch(args[0]) {
   case "BinOver": detector=new br.ufes.inf.nemo.antipattern.binover.BinOverAntipattern(p); break;
   case "DecInt": detector=new br.ufes.inf.nemo.antipattern.decint.DecIntAntipattern(p); break;
   case "DepPhase": detector=new br.ufes.inf.nemo.antipattern.depphase.DepPhaseAntipattern(p); break;
   case "FreeRole": detector=new br.ufes.inf.nemo.antipattern.freerole.FreeRoleAntipattern(p); break;
   case "GSRig": detector=new br.ufes.inf.nemo.antipattern.GSRig.GSRigAntipattern(p); break;
   case "HetColl": detector=new br.ufes.inf.nemo.antipattern.hetcoll.HetCollAntipattern(p); break;
   case "HomoFunc": detector=new br.ufes.inf.nemo.antipattern.homofunc.HomoFuncAntipattern(p); break;
   case "ImpAbs": detector=new br.ufes.inf.nemo.antipattern.impabs.ImpAbsAntipattern(p); break;
   case "MixIden": detector=new br.ufes.inf.nemo.antipattern.mixiden.MixIdenAntipattern(p); break;
   case "MixRig": detector=new br.ufes.inf.nemo.antipattern.mixrig.MixRigAntipattern(p); break;
   case "MultiDep": detector=new br.ufes.inf.nemo.antipattern.multidep.MultiDepAntipattern(p); break;
   case "PartOver": detector=new br.ufes.inf.nemo.antipattern.partover.PartOverAntipattern(p); break;
   case "RelComp": detector=new br.ufes.inf.nemo.antipattern.relcomp.RelCompAntipattern(p); break;
   case "RelOver": detector=new br.ufes.inf.nemo.antipattern.relover.RelOverAntipattern(p); break;
   case "RelRig": detector=new br.ufes.inf.nemo.antipattern.relrig.RelRigAntipattern(p); break;
   case "RelSpec": detector=new br.ufes.inf.nemo.antipattern.relspec.RelSpecAntipattern(p); break;
   case "RepRel": detector=new br.ufes.inf.nemo.antipattern.reprel.RepRelAntipattern(p); break;
   case "UndefFormal": detector=new br.ufes.inf.nemo.antipattern.undefformal.UndefFormalAntipattern(p); break;
   case "UndefPhase": detector=new br.ufes.inf.nemo.antipattern.undefphase.UndefPhaseAntipattern(p); break;
   case "WholeOver": detector=new br.ufes.inf.nemo.antipattern.wholeover.WholeOverAntipattern(p); break;
   default: throw new IllegalArgumentException(args[0]);
  }
  int count=detector.identify().size();
  System.out.println("CMPE_RESULT detector="+args[0]+" classes="+p.getAllInstances(Class.class).size()+" associations="+p.getAllInstances(Association.class).size()+" occurrences="+count);
 }
}
