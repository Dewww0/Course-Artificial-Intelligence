"""
Streamlit interface for the Rule-Based Expert System.
This module provides a web interface for interacting with the expert system.
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from expert_system_core import ExpertSystem, Rule, Fact
from medical_knowledge_base import load_medical_knowledge_base, get_symptom_descriptions
import time

# Initialize expert system
@st.cache_resource
def get_expert_system():
    es = ExpertSystem()
    rules = load_medical_knowledge_base()
    for rule in rules:
        es.add_rule(rule)
    return es

def create_inference_graph(explanations):
    """Create a networkx graph from fact explanations for visualization."""
    G = nx.DiGraph()
    
    if not explanations or explanations[0].get("explanation"):
        return G
    
    for item in explanations:
        if "fact" in item:
            fact = item["fact"]
            G.add_node(fact, type="fact")
            
            # If this fact is derived by a rule, add rule node and connections
            if "derived_by" in item:
                rule_name = item["derived_by"]
                rule_id = f"Rule: {rule_name}"
                G.add_node(rule_id, type="rule", description=item.get("rule_description", ""))
                G.add_edge(rule_id, fact)
                
                # Add antecedents
                for ant in item.get("antecedents", []):
                    G.add_node(ant, type="fact")
                    G.add_edge(ant, rule_id)
    
    return G

def visualize_inference_graph(G):
    """Visualize the inference graph using matplotlib."""
    if not G.nodes():
        return None
    
    plt.figure(figsize=(10, 8))
    
    # Separate fact and rule nodes
    fact_nodes = [node for node, attr in G.nodes(data=True) if attr.get("type") == "fact"]
    rule_nodes = [node for node, attr in G.nodes(data=True) if attr.get("type") == "rule"]
    
    # Position nodes using hierarchical layout
    pos = nx.spring_layout(G, seed=42)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, nodelist=fact_nodes, node_color="lightblue", 
                           node_size=2000, alpha=0.8, node_shape="o")
    nx.draw_networkx_nodes(G, pos, nodelist=rule_nodes, node_color="lightgreen", 
                           node_size=2000, alpha=0.8, node_shape="s")
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, arrows=True)
    
    # Draw labels
    fact_labels = {node: node for node in fact_nodes}
    rule_labels = {node: node for node in rule_nodes}
    nx.draw_networkx_labels(G, pos, labels=fact_labels, font_size=10)
    nx.draw_networkx_labels(G, pos, labels=rule_labels, font_size=10)
    
    plt.title("Inference Explanation Graph", fontsize=16)
    plt.axis("off")
    
    return plt

def main():
    st.set_page_config(page_title="Medical Expert System", page_icon="🏥", layout="wide")
    
    st.title("🏥 Medical Diagnosis Expert System")
    st.markdown("""
    This system demonstrates rule-based reasoning for medical diagnosis using both 
    forward and backward chaining inference techniques.
    """)
    
    expert_system = get_expert_system()
    symptom_descriptions = get_symptom_descriptions()
    
    # Sidebar - System Information
    with st.sidebar:
        st.header("System Information")
        st.info(f"Knowledge Base: {len(expert_system.rules)} rules loaded")
        st.info(f"Working Memory: {len(expert_system.facts)} facts")
        
        st.header("Reset System")
        if st.button("Clear All Facts"):
            expert_system.clear_facts()
            st.success("All facts have been cleared!")
            st.experimental_rerun()
    
    # Main area - tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["Symptom Input", "Forward Chaining", "Backward Chaining", "Explanation"])
    
    # Tab 1: Symptom Input
    with tab1:
        st.header("Patient Symptom Input")
        st.markdown("Select the symptoms the patient is experiencing:")
        
        col1, col2 = st.columns(2)
        
        # Create checkboxes for symptoms
        symptoms = {}
        counter = 0
        for symptom, description in symptom_descriptions.items():
            if counter % 2 == 0:
                column = col1
            else:
                column = col2
                
            with column:
                symptoms[symptom] = st.checkbox(
                    f"{symptom.replace('_', ' ').title()}", 
                    help=description,
                    value=expert_system.fact_exists(symptom)
                )
            counter += 1
        
        if st.button("Submit Symptoms"):
            # Clear previous facts
            expert_system.clear_facts()
            
            # Add selected symptoms as facts
            for symptom, selected in symptoms.items():
                if selected:
                    expert_system.add_fact(Fact(symptom, 1.0, "User input"))
                # For negation symptoms (those starting with "no_")
                elif symptom.startswith("no_") and not selected:
                    actual_symptom = symptom[3:]  # Remove "no_" prefix
                    if actual_symptom in symptoms and symptoms[actual_symptom]:
                        continue  # If the positive symptom is selected, don't add negative
                    expert_system.add_fact(Fact(symptom, 1.0, "User input (negative)"))
            
            st.success("Symptoms recorded successfully!")
            
            # Display current facts
            if expert_system.facts:
                st.subheader("Current Patient Facts:")
                facts_df = pd.DataFrame([
                    {"Fact": fact, "Confidence": f.confidence, "Source": f.source} 
                    for fact, f in expert_system.facts.items()
                ])
                st.dataframe(facts_df, use_container_width=True)
    
    # Tab 2: Forward Chaining
    with tab2:
        st.header("Forward Chaining Inference")
        st.markdown("""
        Forward chaining starts with the known facts (symptoms) and applies rules
        to infer new information until no more inferences can be made.
        """)
        
        if st.button("Run Forward Chaining"):
            if not expert_system.facts:
                st.warning("No facts available. Please add symptoms first.")
            else:
                with st.spinner("Running forward chaining inference..."):
                    start_time = time.time()
                    inference_trace = expert_system.forward_chain()
                    elapsed_time = time.time() - start_time
                    
                    st.success(f"Inference completed in {elapsed_time:.4f} seconds!")
                    
                    # Display inference trace
                    if inference_trace:
                        st.subheader("Inference Process:")
                        for step in inference_trace:
                            with st.expander(f"Step {step['iteration']}: Applied {step['rule_applied']}"):
                                st.markdown(f"**Rule Description**: {step['rule_description']}")
                                st.markdown("**Based on facts**:")
                                for ant in step['antecedents']:
                                    st.markdown(f"- {ant}")
                                st.markdown("**New facts derived**:")
                                for fact in step['new_facts']:
                                    st.markdown(f"- {fact}")
                    else:
                        st.info("No new facts could be inferred from the provided symptoms.")
                        
                    # Display resulting diagnoses
                    diagnoses = [fact for fact in expert_system.facts 
                                if fact in ['flu', 'covid', 'cold', 'allergy']]
                    recommendations = [fact for fact in expert_system.facts 
                                     if fact.startswith('recommend_') or fact.startswith('consider_') 
                                     or fact.startswith('monitor_') or fact.startswith('avoid_')]
                    
                    if diagnoses:
                        st.subheader("Diagnoses:")
                        for diagnosis in diagnoses:
                            conf = expert_system.facts[diagnosis].confidence
                            st.markdown(f"- **{diagnosis.upper()}** (confidence: {conf:.2f})")
                    
                    if recommendations:
                        st.subheader("Recommendations:")
                        for rec in recommendations:
                            st.markdown(f"- {rec.replace('_', ' ').title()}")
    
    # Tab 3: Backward Chaining
    with tab3:
        st.header("Backward Chaining Inference")
        st.markdown("""
        Backward chaining starts with a goal (possible diagnosis) and works backwards
        to determine if the known facts support that diagnosis.
        """)
        
        possible_goals = ['flu', 'covid', 'cold', 'allergy', 
                         'recommend_rest', 'recommend_covid_test',
                         'unlikely_flu', 'unlikely_covid']
        
        selected_goal = st.selectbox(
            "Select diagnosis or recommendation to verify:",
            possible_goals,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        if st.button("Verify Goal"):
            if not expert_system.facts:
                st.warning("No facts available. Please add symptoms first.")
            else:
                with st.spinner(f"Verifying if '{selected_goal}' can be proven..."):
                    start_time = time.time()
                    is_proven, trace = expert_system.backward_chain(selected_goal)
                    elapsed_time = time.time() - start_time
                    
                    if is_proven:
                        st.success(f"✅ The goal '{selected_goal}' was proven! (in {elapsed_time:.4f} seconds)")
                        conf = expert_system.facts[selected_goal].confidence
                        st.info(f"Confidence: {conf:.2f}")
                    else:
                        st.error(f"❌ The goal '{selected_goal}' could not be proven with the available facts.")
                    
                    # Display trace
                    st.subheader("Reasoning Process:")
                    for step in trace:
                        if 'rule' in step:
                            with st.expander(f"Examining rule: {step['rule']}"):
                                st.markdown(f"**Description**: {step.get('description', 'No description')}")
                                st.markdown(f"**Goal to prove**: {step['goal']}")
                                st.markdown("**Needs to prove**:")
                                for need in step.get('needs_to_prove', []):
                                    st.markdown(f"- {need}")
                        else:
                            status_color = "green" if step.get('status') == "Proven" else "red"
                            with st.expander(f"{step.get('step', 'Step')} - {step.get('status', '')}"):
                                st.markdown(f"**Goal**: {step.get('goal', 'N/A')}")
                                st.markdown(f"**Result**: {step.get('result', 'N/A')}")
                                st.markdown(f"**Status**: :{status_color}[{step.get('status', 'N/A')}]")
    
    # Tab 4: Explanation
    with tab4:
        st.header("Explanation Facility")
        st.markdown("""
        This tab explains how facts were derived in the expert system,
        showing the chain of rules and reasoning.
        """)
        
        # Only display facts that were derived, not initial inputs
        derived_facts = [fact for fact, f in expert_system.facts.items() 
                        if f.source and not f.source.startswith("User input")]
        
        if not derived_facts:
            st.info("No derived facts to explain. Please run inference first.")
        else:
            selected_fact = st.selectbox(
                "Select a fact to explain:",
                derived_facts,
                format_func=lambda x: x.replace('_', ' ').title()
            )
            
            if st.button("Explain Fact"):
                explanations = expert_system.explain_fact(selected_fact)
                
                st.subheader(f"Explanation for: {selected_fact}")
                
                # Text explanation
                for item in explanations:
                    if "explanation" in item:
                        st.info(item["explanation"])
                    else:
                        with st.expander(f"Fact: {item['fact']}"):
                            if "derived_by" in item:
                                st.markdown(f"**Derived by rule**: {item['derived_by']}")
                                st.markdown(f"**Rule description**: {item['rule_description']}")
                                st.markdown(f"**Confidence**: {item['confidence']:.2f}")
                                st.markdown("**Based on facts**:")
                                for ant in item.get("antecedents", []):
                                    st.markdown(f"- {ant}")
                            elif "proven_by" in item:
                                st.markdown(f"**Proven by rule**: {item['proven_by']}")
                                st.markdown(f"**Rule description**: {item['rule_description']}")
                                st.markdown(f"**Confidence**: {item['confidence']:.2f}")
                                st.markdown("**Antecedents proven**:")
                                for ant in item.get("antecedents_proven", []):
                                    st.markdown(f"- {ant}")
                
                # Visual explanation
                G = create_inference_graph(explanations)
                if G.nodes():
                    st.subheader("Visual Explanation")
                    vis_plot = visualize_inference_graph(G)
                    if vis_plot:
                        st.pyplot(vis_plot)

if __name__ == "__main__":
    main()