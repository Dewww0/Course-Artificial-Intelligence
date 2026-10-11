"""
Rule-Based Expert System Core Implementation
This module contains the core functionality of the rule-based expert system
implementing both forward and backward chaining inference mechanisms.
"""
import copy
from typing import Dict, List, Set, Tuple, Optional, Any


class Rule:
    """
    Represents a rule in the knowledge base.
    A rule consists of antecedents (IF part) and consequents (THEN part).
    """
    def __init__(self, name: str, antecedents: List[str], consequents: List[str], description: str = ""):
        self.name = name
        self.antecedents = antecedents  # List of conditions that must be true
        self.consequents = consequents  # List of facts to be asserted when rule fires
        self.description = description  # Human-readable description of the rule

    def __str__(self) -> str:
        return f"Rule {self.name}: IF {' AND '.join(self.antecedents)} THEN {' AND '.join(self.consequents)}"


class Fact:
    """
    Represents a fact in the working memory.
    A fact can have a confidence level and source information.
    """
    def __init__(self, statement: str, confidence: float = 1.0, source: str = ""):
        self.statement = statement
        self.confidence = confidence  # Confidence level (0.0 to 1.0)
        self.source = source  # Origin of the fact (user input, rule inference, etc.)
        
    def __str__(self) -> str:
        return f"{self.statement} [conf={self.confidence:.2f}, src={self.source}]"


class ExpertSystem:
    """
    The core expert system class that implements both forward and backward chaining.
    """
    def __init__(self):
        self.rules: Dict[str, Rule] = {}
        self.facts: Dict[str, Fact] = {}
        self.inference_trace: List[Dict[str, Any]] = []
        
    def add_rule(self, rule: Rule) -> None:
        """Add a rule to the knowledge base."""
        self.rules[rule.name] = rule
        
    def add_fact(self, fact: Fact) -> None:
        """Add a fact to the working memory."""
        self.facts[fact.statement] = fact
        
    def clear_facts(self) -> None:
        """Clear all facts from working memory."""
        self.facts = {}
        
    def clear_inference_trace(self) -> None:
        """Clear the inference trace."""
        self.inference_trace = []
    
    def fact_exists(self, statement: str) -> bool:
        """Check if a fact exists in the working memory."""
        return statement in self.facts
    
    def forward_chain(self) -> List[Dict[str, Any]]:
        """
        Execute forward chaining inference.
        Returns a trace of the inference process.
        """
        self.clear_inference_trace()
        
        # Continue until no new facts are added
        new_facts_added = True
        iteration = 0
        
        while new_facts_added:
            iteration += 1
            new_facts_added = False
            applicable_rules = []
            
            # Find applicable rules
            for rule_name, rule in self.rules.items():
                # Skip rules that have already been applied (all consequents are facts)
                if all(self.fact_exists(consequent) for consequent in rule.consequents):
                    continue
                    
                # Check if all antecedents are satisfied
                if all(self.fact_exists(antecedent) for antecedent in rule.antecedents):
                    applicable_rules.append(rule)
            
            # No applicable rules found, stop inference
            if not applicable_rules:
                break
                
            # Apply rules and add new facts
            for rule in applicable_rules:
                new_facts_in_rule = False
                for consequent in rule.consequents:
                    if not self.fact_exists(consequent):
                        # Calculate confidence as minimum of antecedent confidences
                        antecedent_confidences = [self.facts[ant].confidence for ant in rule.antecedents]
                        confidence = min(antecedent_confidences) if antecedent_confidences else 1.0
                        
                        new_fact = Fact(consequent, confidence, f"Rule: {rule.name}")
                        self.add_fact(new_fact)
                        new_facts_added = True
                        new_facts_in_rule = True
                
                if new_facts_in_rule:
                    self.inference_trace.append({
                        "iteration": iteration,
                        "rule_applied": rule.name,
                        "rule_description": rule.description,
                        "antecedents": [str(self.facts[ant]) for ant in rule.antecedents],
                        "new_facts": [str(self.facts[con]) for con in rule.consequents 
                                     if self.facts[con].source == f"Rule: {rule.name}"]
                    })
        
        return self.inference_trace
    
    def backward_chain(self, goal: str) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Execute backward chaining to determine if a goal can be proven.
        Returns a tuple of (goal_proven, inference_trace).
        """
        self.clear_inference_trace()
        
        # If goal is already a known fact, return true
        if self.fact_exists(goal):
            self.inference_trace.append({
                "step": "Goal verification",
                "result": f"Goal '{goal}' is already a known fact",
                "status": "Proven"
            })
            return True, self.inference_trace
        
        # Track goals to prevent infinite recursion
        visited_goals = set()
        return self._backward_chain_recursive(goal, visited_goals, 1)
    
    def _backward_chain_recursive(self, goal: str, visited_goals: Set[str], depth: int) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Recursive helper for backward chaining.
        """
        if goal in visited_goals:
            self.inference_trace.append({
                "step": f"Recursion check at depth {depth}",
                "goal": goal,
                "result": "Circular reasoning detected",
                "status": "Failed"
            })
            return False, self.inference_trace
        
        visited_goals.add(goal)
        
        # Find rules that have this goal as a consequent
        relevant_rules = []
        for rule in self.rules.values():
            if goal in rule.consequents:
                relevant_rules.append(rule)
        
        if not relevant_rules:
            self.inference_trace.append({
                "step": f"Goal exploration at depth {depth}",
                "goal": goal,
                "result": "No rules found that infer this goal",
                "status": "Failed" if not self.fact_exists(goal) else "Proven"
            })
            return self.fact_exists(goal), self.inference_trace
        
        # Try each rule
        for rule in relevant_rules:
            self.inference_trace.append({
                "step": f"Rule examination at depth {depth}",
                "rule": rule.name,
                "description": rule.description,
                "goal": goal,
                "needs_to_prove": rule.antecedents
            })
            
            # Check if all antecedents can be satisfied
            all_antecedents_satisfied = True
            for antecedent in rule.antecedents:
                if not self.fact_exists(antecedent):
                    # Recursively try to prove this antecedent
                    antecedent_proven, _ = self._backward_chain_recursive(antecedent, copy.deepcopy(visited_goals), depth + 1)
                    if not antecedent_proven:
                        all_antecedents_satisfied = False
                        break
            
            if all_antecedents_satisfied:
                # Add the goal as a proven fact
                if not self.fact_exists(goal):
                    # Calculate confidence based on antecedent confidences
                    antecedent_confidences = [self.facts[ant].confidence for ant in rule.antecedents]
                    confidence = min(antecedent_confidences) if antecedent_confidences else 1.0
                    self.add_fact(Fact(goal, confidence, f"Backward chaining: {rule.name}"))
                
                self.inference_trace.append({
                    "step": f"Goal verification at depth {depth}",
                    "goal": goal,
                    "rule_used": rule.name,
                    "result": "All antecedents satisfied",
                    "status": "Proven"
                })
                return True, self.inference_trace
        
        self.inference_trace.append({
            "step": f"Goal verification at depth {depth}",
            "goal": goal,
            "result": "No applicable rules could satisfy all conditions",
            "status": "Failed"
        })
        return False, self.inference_trace

    def explain_fact(self, fact_statement: str) -> List[Dict[str, Any]]:
        """
        Provides an explanation of how a fact was derived.
        """
        if not self.fact_exists(fact_statement):
            return [{"explanation": f"Fact '{fact_statement}' does not exist in working memory."}]
        
        fact = self.facts[fact_statement]
        if fact.source == "":
            return [{"explanation": f"Fact '{fact_statement}' was directly provided as input."}]
            
        explanation = []
        if fact.source.startswith("Rule:"):
            rule_name = fact.source.split(": ")[1]
            if rule_name in self.rules:
                rule = self.rules[rule_name]
                explanation.append({
                    "fact": fact_statement,
                    "derived_by": rule_name,
                    "rule_description": rule.description,
                    "confidence": fact.confidence,
                    "antecedents": rule.antecedents
                })
                
                # Recursively explain each antecedent
                for antecedent in rule.antecedents:
                    explanation.extend(self.explain_fact(antecedent))
        
        elif fact.source.startswith("Backward chaining:"):
            rule_name = fact.source.split(": ")[1]
            if rule_name in self.rules:
                rule = self.rules[rule_name]
                explanation.append({
                    "fact": fact_statement,
                    "proven_by": rule_name,
                    "rule_description": rule.description,
                    "confidence": fact.confidence,
                    "antecedents_proven": rule.antecedents
                })
                
                # Recursively explain each antecedent
                for antecedent in rule.antecedents:
                    explanation.extend(self.explain_fact(antecedent))
        
        return explanation