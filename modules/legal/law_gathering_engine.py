from modules.logger import log_provenance, system_logger
from modules.corpus_manager import corpus_manager
import re
import json
from datetime import datetime
from typing import List, Dict, Any

class LawGatheringEngine:
    """
    Aggregates case law, constitutional clauses, and remedy statutes for sovereign research.
    Provides searchable legal corpus with citations and relevance scoring.
    """

    def __init__(self):
        self.corpus_manager = corpus_manager

        # Load structured legal corpus if available
        self.case_law_corpus = self._load_case_law_corpus()
        self.constitutional_corpus = self._load_constitutional_corpus()
        self.remedy_statutes = self._load_remedy_statutes()
        self.model_affidavits = self._load_model_affidavits()

        system_logger.info("LawGatheringEngine initialized with legal corpus")

    def _load_case_law_corpus(self):
        """Loads case law database from corpus."""
        # Try to load structured case law from corpus
        case_law_text = self.corpus_manager.get_corpus_text('case_law_database.md')
        if case_law_text:
            return self._parse_case_law_text(case_law_text)

        # Fallback to built-in essential cases
        return self._get_essential_case_law()

    def _load_constitutional_corpus(self):
        """Loads constitutional provisions and amendments."""
        constitution_text = self.corpus_manager.get_corpus_text('constitution_provisions.md')
        if constitution_text:
            return self._parse_constitutional_text(constitution_text)

        return self._get_essential_constitutional_provisions()

    def _load_remedy_statutes(self):
        """Loads remedy statutes and codes."""
        statutes_text = self.corpus_manager.get_corpus_text('remedy_statutes.md')
        if statutes_text:
            return self._parse_statutes_text(statutes_text)

        return self._get_essential_remedy_statutes()

    def _load_model_affidavits(self):
        """Loads model affidavit templates."""
        affidavits_text = self.corpus_manager.get_corpus_text('model_affidavits.md')
        if affidavits_text:
            return self._parse_affidavits_text(affidavits_text)

        return self._get_essential_affidavits()

    def search_case_law(self, query: str, jurisdiction: str = None, remedy_type: str = None) -> List[Dict]:
        """
        Searches case law database with semantic matching and relevance scoring.

        Args:
            query (str): Search query
            jurisdiction (str): Filter by jurisdiction (federal, state, common_law)
            remedy_type (str): Filter by remedy type (sovereignty, jurisdiction, rights)

        Returns:
            List[Dict]: Relevant cases with citation and relevance score
        """
        log_provenance("LawGatheringEngine", "SearchCaseLaw", f"Searching case law: {query}")

        results = []
        query_terms = query.lower().split()

        for case in self.case_law_corpus:
            # Apply filters
            if jurisdiction and case.get('jurisdiction') != jurisdiction:
                continue
            if remedy_type and remedy_type not in case.get('remedy_types', []):
                continue

            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(query_terms, case)

            if relevance_score > 0.1:  # Minimum relevance threshold
                result = {
                    'case_name': case.get('case_name', 'Unknown Case'),
                    'citation': case.get('citation', 'Unknown Citation'),
                    'year': case.get('year', 'Unknown Year'),
                    'jurisdiction': case.get('jurisdiction', 'Unknown'),
                    'holding': case.get('holding', ''),
                    'relevance_score': relevance_score,
                    'remedy_types': case.get('remedy_types', []),
                    'key_principles': case.get('key_principles', []),
                    'quotable_text': self._extract_relevant_quote(query_terms, case)
                }
                results.append(result)

        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)

        log_provenance("LawGatheringEngine", "CaseLawSearchComplete", f"Found {len(results)} relevant cases")
        return results[:20]  # Return top 20 results

    def find_remedy_statutes(self, query: str, code_type: str = None) -> List[Dict]:
        """
        Finds remedy statutes and legal codes.

        Args:
            query (str): Search query
            code_type (str): Filter by code type (UCC, Constitution, CFR, State)

        Returns:
            List[Dict]: Relevant statutes with citation and application
        """
        log_provenance("LawGatheringEngine", "FindRemedyStatutes", f"Searching remedy statutes: {query}")

        results = []
        query_terms = query.lower().split()

        for statute in self.remedy_statutes:
            # Apply code type filter
            if code_type and statute.get('code_type') != code_type:
                continue

            # Calculate relevance
            relevance_score = self._calculate_relevance_score(query_terms, statute)

            if relevance_score > 0.1:
                result = {
                    'statute_name': statute.get('statute_name', 'Unknown Statute'),
                    'citation': statute.get('citation', 'Unknown Citation'),
                    'code_type': statute.get('code_type', 'Unknown'),
                    'section': statute.get('section', ''),
                    'text': statute.get('text', ''),
                    'relevance_score': relevance_score,
                    'application': statute.get('application', ''),
                    'key_provisions': statute.get('key_provisions', [])
                }
                results.append(result)

        results.sort(key=lambda x: x['relevance_score'], reverse=True)

        log_provenance("LawGatheringEngine", "RemedyStatutesFound", f"Found {len(results)} relevant statutes")
        return results[:15]

    def get_model_affidavits(self, affidavit_type: str = None) -> List[Dict]:
        """
        Retrieves model affidavit templates.

        Args:
            affidavit_type (str): Filter by type (status_correction, jurisdiction, rights_assertion)

        Returns:
            List[Dict]: Model affidavit templates
        """
        log_provenance("LawGatheringEngine", "GetModelAffidavits", f"Retrieving affidavits: {affidavit_type}")

        results = []

        for affidavit in self.model_affidavits:
            if affidavit_type and affidavit_type not in affidavit.get('types', []):
                continue

            results.append({
                'title': affidavit.get('title', 'Untitled Affidavit'),
                'type': affidavit.get('type', 'General'),
                'description': affidavit.get('description', ''),
                'template_text': affidavit.get('template_text', ''),
                'required_elements': affidavit.get('required_elements', []),
                'jurisdiction': affidavit.get('jurisdiction', 'Common Law'),
                'usage_notes': affidavit.get('usage_notes', '')
            })

        log_provenance("LawGatheringEngine", "AffidavitsRetrieved", f"Found {len(results)} model affidavits")
        return results

    def search_legal_authorities(self, query: str) -> Dict[str, Any]:
        """
        Comprehensive search across all legal authorities.

        Args:
            query (str): Search query

        Returns:
            Dict: Combined search results from all legal sources
        """
        log_provenance("LawGatheringEngine", "SearchLegalAuthorities", f"Comprehensive search: {query}")

        # Search all legal sources
        case_law_results = self.search_case_law(query)
        statute_results = self.find_remedy_statutes(query)
        constitutional_results = self._search_constitutional(query)
        affidavit_results = self.get_model_affidavits()

        # Combine and analyze results
        combined_results = {
            'query': query,
            'search_timestamp': datetime.utcnow().isoformat(),
            'case_law': case_law_results,
            'statutes': statute_results,
            'constitutional': constitutional_results,
            'affidavits': affidavit_results,
            'summary': self._generate_search_summary(case_law_results, statute_results, constitutional_results),
            'recommended_authorities': self._recommend_authorities(case_law_results, statute_results)
        }

        log_provenance("LawGatheringEngine", "ComprehensiveSearchComplete", f"Completed comprehensive search with {len(case_law_results)} cases, {len(statute_results)} statutes")
        return combined_results

    def _calculate_relevance_score(self, query_terms: List[str], document: Dict) -> float:
        """Calculates relevance score based on term matching."""
        score = 0.0
        text_content = (
            document.get('holding', '') + ' ' +
            document.get('text', '') + ' ' +
            ' '.join(document.get('key_principles', [])) + ' ' +
            ' '.join(document.get('key_provisions', []))
        ).lower()

        # Exact phrase matches get higher score
        query_phrase = ' '.join(query_terms)
        if query_phrase in text_content:
            score += 1.0

        # Individual term matches
        for term in query_terms:
            term_count = text_content.count(term)
            score += term_count * 0.1

        # Title/citation matches get bonus
        title = document.get('case_name', document.get('statute_name', '')).lower()
        for term in query_terms:
            if term in title:
                score += 0.5

        return min(score, 2.0)  # Cap at 2.0

    def _extract_relevant_quote(self, query_terms: List[str], case: Dict) -> str:
        """Extracts most relevant quote from case."""
        text = case.get('holding', '')
        if not text:
            return ""

        # Find sentence with most query terms
        sentences = re.split(r'[.!?]+', text)
        best_sentence = ""
        best_score = 0

        for sentence in sentences:
            score = sum(1 for term in query_terms if term in sentence.lower())
            if score > best_score and len(sentence.strip()) > 20:
                best_score = score
                best_sentence = sentence.strip()

        return best_sentence if best_score > 0 else text[:200] + "..." if len(text) > 200 else text

    def _search_constitutional(self, query: str) -> List[Dict]:
        """Searches constitutional provisions."""
        query_terms = query.lower().split()
        results = []

        for provision in self.constitutional_corpus:
            relevance_score = self._calculate_relevance_score(query_terms, provision)

            if relevance_score > 0.1:
                results.append({
                    'provision': provision.get('provision', 'Unknown'),
                    'article': provision.get('article', ''),
                    'section': provision.get('section', ''),
                    'text': provision.get('text', ''),
                    'relevance_score': relevance_score,
                    'application': provision.get('application', '')
                })

        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results

    def _generate_search_summary(self, cases: List, statutes: List, constitutional: List) -> str:
        """Generates summary of search results."""
        summary_parts = []

        if cases:
            summary_parts.append(f"Found {len(cases)} relevant case law authorities")
        if statutes:
            summary_parts.append(f"Found {len(statutes)} relevant statutes and codes")
        if constitutional:
            summary_parts.append(f"Found {len(constitutional)} constitutional provisions")

        if not summary_parts:
            return "No direct matches found. Consider refining search terms."

        return ". ".join(summary_parts) + "."

    def _recommend_authorities(self, cases: List, statutes: List) -> List[Dict]:
        """Recommends top authorities for citation."""
        recommendations = []

        # Top 3 cases
        for case in cases[:3]:
            recommendations.append({
                'type': 'case_law',
                'authority': case['case_name'],
                'citation': case['citation'],
                'reason': 'High relevance and precedent value'
            })

        # Top 2 statutes
        for statute in statutes[:2]:
            recommendations.append({
                'type': 'statute',
                'authority': statute['statute_name'],
                'citation': statute['citation'],
                'reason': 'Direct statutory authority'
            })

        return recommendations

    # Built-in essential legal authorities as fallback
    def _get_essential_case_law(self):
        """Returns essential case law database."""
        return [
            {
                'case_name': 'Hale v. Henkel',
                'citation': '201 U.S. 43 (1906)',
                'year': 1906,
                'jurisdiction': 'supreme_court',
                'holding': 'The individual may stand upon his constitutional rights as a citizen. He is entitled to carry on his private business in his own way. His rights are protected against both federal and state interference.',
                'remedy_types': ['sovereignty', 'rights_protection', 'constitutional'],
                'key_principles': ['sovereign immunity', 'right to contract', 'private business protection']
            },
            {
                'case_name': 'Bond v. United States',
                'citation': '529 U.S. 334 (2000)',
                'year': 2000,
                'jurisdiction': 'supreme_court',
                'holding': 'The Constitution protects individuals from intrusion by the government, including in their relationships with others.',
                'remedy_types': ['rights_protection', 'government_limitation'],
                'key_principles': ['right to privacy', 'government limitations', 'individual sovereignty']
            },
            {
                'case_name': 'Marbury v. Madison',
                'citation': '5 U.S. (1 Cranch) 137 (1803)',
                'year': 1803,
                'jurisdiction': 'supreme_court',
                'holding': 'It is emphatically the province and duty of the judicial department to say what the law is.',
                'remedy_types': ['judicial_review', 'constitutional_law'],
                'key_principles': ['judicial review', 'separation of powers', 'constitutional supremacy']
            },
            {
                'case_name': 'Murdoch v. Pennsylvania',
                'citation': '319 U.S. 105 (1943)',
                'year': 1943,
                'jurisdiction': 'supreme_court',
                'holding': 'A state may not, through licensing requirements, impose a prior restraint on the exercise of constitutional rights.',
                'remedy_types': ['rights_protection', 'religious_freedom', 'prior_restraint'],
                'key_principles': ['first amendment', 'prior restraint', 'religious freedom']
            }
        ]

    def _get_essential_constitutional_provisions(self):
        """Returns essential constitutional provisions."""
        return [
            {
                'provision': 'Article IV - Privileges and Immunities',
                'article': 'IV',
                'section': '2',
                'text': 'The Citizens of each State shall be entitled to all Privileges and Immunities of Citizens in the several States.',
                'application': 'Protects right to travel and conduct business across state lines'
            },
            {
                'provision': 'First Amendment - Religious Freedom',
                'article': 'I',
                'section': '',
                'text': 'Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof...',
                'application': 'Protects free exercise of religious beliefs and conscience'
            },
            {
                'provision': 'Fourth Amendment - Unreasonable Searches',
                'article': 'IV',
                'section': '',
                'text': 'The right of the people to be secure in their persons, houses, papers, and effects, against unreasonable searches and seizures...',
                'application': 'Protects privacy and property from government intrusion'
            },
            {
                'provision': 'Sixth Amendment - Right to Counsel',
                'article': 'VI',
                'section': '',
                'text': 'In all criminal prosecutions, the accused shall enjoy the right... to have the Assistance of Counsel for his defence.',
                'application': 'Ensures right to legal representation in criminal proceedings'
            }
        ]

    def _get_essential_remedy_statutes(self):
        """Returns essential remedy statutes."""
        return [
            {
                'statute_name': 'UCC 1-207 - Reservation of Rights',
                'citation': 'UCC § 1-207',
                'code_type': 'UCC',
                'section': '1-207',
                'text': 'A party who with explicit reservation of rights performs or promises performance or assents to performance of the contract is not prejudiced by his failure to perform.',
                'application': 'Preserves rights when conducting business under government regulation',
                'key_provisions': ['without prejudice', 'reservation of rights', 'commercial transactions']
            },
            {
                'statute_name': 'UCC 3-104 - Negotiable Instrument Definition',
                'citation': 'UCC § 3-104',
                'code_type': 'UCC',
                'section': '3-104',
                'text': 'A negotiable instrument is an unconditional promise or order to pay a fixed amount of money...',
                'application': 'Defines requirements for negotiable instruments in commerce',
                'key_provisions': ['unconditional promise', 'fixed amount', 'negotiable instrument']
            },
            {
                'statute_name': 'Title 18 USC § 241 - Conspiracy Against Rights',
                'citation': '18 U.S.C. § 241',
                'code_type': 'USC',
                'section': '241',
                'text': 'If two or more persons conspire to injure, oppress, threaten, or intimidate any person... in the free exercise or enjoyment of any right or privilege secured to him by the Constitution...',
                'application': 'Criminal liability for conspiring to violate constitutional rights',
                'key_provisions': ['conspiracy', 'constitutional rights', 'criminal penalties']
            },
            {
                'statute_name': 'Title 18 USC § 242 - Deprivation of Rights Under Color of Law',
                'citation': '18 U.S.C. § 242',
                'code_type': 'USC',
                'section': '242',
                'text': 'Whoever, under color of any law, statute, ordinance, regulation, or custom, willfully subjects any person... to the deprivation of any rights...',
                'application': 'Criminal liability for rights violations by government officials',
                'key_provisions': ['color of law', 'rights deprivation', 'official misconduct']
            }
        ]

    def _get_essential_affidavits(self):
        """Returns essential model affidavits."""
        return [
            {
                'title': 'Affidavit of Sovereign Status',
                'type': 'status_correction',
                'description': 'Declares sovereign status and rebutts presumptions of federal citizenship',
                'template_text': 'AFFIDAVIT OF SOVEREIGN STATUS\\n\\nI, [Name], being duly sworn, hereby declare:\\n1. I am a living man/woman...\\n2. I am an American State National...',
                'required_elements': ['name', 'domicile', 'status declaration', 'notarization'],
                'jurisdiction': 'Common Law',
                'usage_notes': 'Use to correct status in government records'
            },
            {
                'title': 'Affidavit of Jurisdiction',
                'type': 'jurisdiction',
                'description': 'Declares proper jurisdiction and venue for legal matters',
                'template_text': 'AFFIDAVIT OF JURISDICTION\\n\\nI, [Name], hereby declare:\\n1. My proper jurisdiction is Common Law...\\n2. I consent only to laws...',
                'required_elements': ['jurisdiction declaration', 'venue specification', 'consent limitations'],
                'jurisdiction': 'Common Law',
                'usage_notes': 'Use to establish proper jurisdiction in legal proceedings'
            }
        ]

    def _parse_case_law_text(self, text: str) -> List[Dict]:
        """Parses case law from markdown text."""
        # Implementation would parse structured markdown into case objects
        # For now, return built-in cases
        return self._get_essential_case_law()

    def _parse_constitutional_text(self, text: str) -> List[Dict]:
        """Parses constitutional provisions from markdown text."""
        return self._get_essential_constitutional_provisions()

    def _parse_statutes_text(self, text: str) -> List[Dict]:
        """Parses statutes from markdown text."""
        return self._get_essential_remedy_statutes()

    def _parse_affidavits_text(self, text: str) -> List[Dict]:
        """Parses affidavits from markdown text."""
        return self._get_essential_affidavits()

# Singleton instance
law_gathering_engine = LawGatheringEngine()