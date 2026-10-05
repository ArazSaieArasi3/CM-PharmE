import java.io.File;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.profiles.*;
import org.semanticweb.owlapi.reasoner.*;
import com.clarkparsia.pellet.owlapiv3.PelletReasonerFactory;

public class CheckOWL2DL {
  public static void main(String[] args) throws Exception {
    OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
    OWLOntology ontology = manager.loadOntologyFromOntologyDocument(new File(args[0]));
    OWLProfileReport report = new OWL2DLProfile().checkOntology(ontology);
    System.out.println("IN_OWL2_DL=" + report.isInProfile());
    System.out.println("VIOLATIONS=" + report.getViolations().size());
    for (OWLProfileViolation v : report.getViolations()) System.out.println(v.toString());
    if (!report.isInProfile()) System.exit(1);
    OWLReasoner reasoner = PelletReasonerFactory.getInstance().createReasoner(ontology);
    boolean consistent = reasoner.isConsistent();
    System.out.println("CONSISTENT=" + consistent);
    if (!consistent) System.exit(2);
    reasoner.precomputeInferences(InferenceType.CLASS_HIERARCHY);
    java.util.Set<OWLClass> unsat = reasoner.getUnsatisfiableClasses().getEntitiesMinusBottom();
    System.out.println("UNSAT_CLASSES=" + unsat.size());
    for (OWLClass c : unsat) System.out.println("UNSAT=" + c.getIRI());
    reasoner.dispose();
    if (!unsat.isEmpty()) System.exit(3);
  }
}
