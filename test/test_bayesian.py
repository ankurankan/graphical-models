"""!
Test Bayesian Network
"""

from gmodels.bayesian import BayesianNetwork
from gmodels.gtypes.edge import Edge, EdgeType
from gmodels.factor import Factor
from gmodels.randomvariable import NumCatRVariable
from uuid import uuid4

import unittest


class BayesianNetworkTest(unittest.TestCase):
    ""

    def setUp(self):
        ""
        idata = {
            "rain": {"outcome-values": [True, False]},
            "sprink": {"outcome-values": [True, False]},
            "wet": {"outcome-values": [True, False]},
        }
        self.rain = NumCatRVariable(
            input_data=idata["rain"],
            node_id="rain",
            distribution=lambda x: 0.2 if x is True else 0.8,
        )
        self.sprink = NumCatRVariable(
            node_id="sprink",
            input_data=idata["sprink"],
            distribution=lambda x: 0.6 if x is True else 0.4,
        )
        self.wet = NumCatRVariable(
            node_id="wet",
            input_data=idata["wet"],
            distribution=lambda x: 0.7 if x is True else 0.3,
        )
        self.rain_wet = Edge(
            edge_id="rain_wet",
            start_node=self.rain,
            end_node=self.wet,
            edge_type=EdgeType.DIRECTED,
        )
        self.rain_sprink = Edge(
            edge_id="rain_sprink",
            start_node=self.rain,
            end_node=self.sprink,
            edge_type=EdgeType.DIRECTED,
        )
        self.sprink_wet = Edge(
            edge_id="sprink_wet",
            start_node=self.sprink,
            end_node=self.wet,
            edge_type=EdgeType.DIRECTED,
        )

        def sprink_rain_factor(scope_product):
            ""
            sfs = set(scope_product)
            if sfs == set([("rain", True), ("sprink", True)]):
                return 0.01
            elif sfs == set([("rain", True), ("sprink", False)]):
                return 0.99
            elif sfs == set([("rain", False), ("sprink", True)]):
                return 0.4
            elif sfs == set([("rain", False), ("sprink", False)]):
                return 0.6
            else:
                raise ValueError("unknown product")

        self.rain_sprink_f = Factor.from_conditional_vars(
            X_i=self.sprink, Pa_Xi=set([self.rain]), fn=sprink_rain_factor
        )

        def grass_wet_factor(scope_product):
            ""
            sfs = set(scope_product)
            if sfs == set([("rain", False), ("sprink", False), ("wet", True)]):
                return 0.0
            elif sfs == set([("rain", False), ("sprink", False), ("wet", False)]):
                return 1.0
            elif sfs == set([("rain", False), ("sprink", True), ("wet", True)]):
                return 0.8
            elif sfs == set([("rain", False), ("sprink", True), ("wet", False)]):
                return 0.2
            elif sfs == set([("rain", True), ("sprink", False), ("wet", True)]):
                return 0.9
            elif sfs == set([("rain", True), ("sprink", False), ("wet", False)]):
                return 0.1
            elif sfs == set([("rain", True), ("sprink", True), ("wet", True)]):
                return 0.99
            elif sfs == set([("rain", True), ("sprink", True), ("wet", False)]):
                return 0.01
            else:
                raise ValueError("unknown product")

        self.grass_wet_f = Factor.from_conditional_vars(
            X_i=self.wet, Pa_Xi=set([self.rain, self.sprink]), fn=grass_wet_factor
        )

        self.bayes = BayesianNetwork(
            gid="b",
            nodes=set([self.rain, self.sprink, self.wet]),
            edges=set([self.rain_wet, self.rain_sprink, self.sprink_wet]),
            factors=set([self.grass_wet_f, self.rain_sprink_f]),
        )
        idata = {"outcome-values": [True, False]}

        self.C = NumCatRVariable(
            node_id="C", input_data=idata, distribution=lambda x: 0.5
        )
        self.E = NumCatRVariable(
            node_id="E", input_data=idata, distribution=lambda x: 0.5
        )
        self.F = NumCatRVariable(
            node_id="F", input_data=idata, distribution=lambda x: 0.5
        )
        self.D = NumCatRVariable(
            node_id="D", input_data=idata, distribution=lambda x: 0.5
        )
        self.CE = Edge(
            edge_id="CE",
            start_node=self.C,
            end_node=self.E,
            edge_type=EdgeType.DIRECTED,
        )
        self.ED = Edge(
            edge_id="ED",
            start_node=self.E,
            end_node=self.D,
            edge_type=EdgeType.DIRECTED,
        )
        self.EF = Edge(
            edge_id="EF",
            start_node=self.E,
            end_node=self.F,
            edge_type=EdgeType.DIRECTED,
        )

        def phi_c(scope_product):
            ss = set(scope_product)
            if ss == set([("C", True)]):
                return 0.8
            elif ss == set([("C", False)]):
                return 0.2
            else:
                raise ValueError("scope product unknown")

        def phi_ec(scope_product):
            ss = set(scope_product)
            if ss == set([("C", True), ("E", True)]):
                return 0.9
            elif ss == set([("C", True), ("E", False)]):
                return 0.1
            elif ss == set([("C", False), ("E", True)]):
                return 0.7
            elif ss == set([("C", False), ("E", False)]):
                return 0.3
            else:
                raise ValueError("scope product unknown")

        def phi_fe(scope_product):
            ss = set(scope_product)
            if ss == set([("E", True), ("F", True)]):
                return 0.9
            elif ss == set([("E", True), ("F", False)]):
                return 0.1
            elif ss == set([("E", False), ("F", True)]):
                return 0.5
            elif ss == set([("E", False), ("F", False)]):
                return 0.5
            else:
                raise ValueError("scope product unknown")

        def phi_de(scope_product):
            ss = set(scope_product)
            if ss == set([("E", True), ("D", True)]):
                return 0.7
            elif ss == set([("E", True), ("D", False)]):
                return 0.3
            elif ss == set([("E", False), ("D", True)]):
                return 0.4
            elif ss == set([("E", False), ("D", False)]):
                return 0.6
            else:
                raise ValueError("scope product unknown")

        self.CE_f = Factor(
            gid="CE_f", scope_vars=set([self.C, self.E]), factor_fn=phi_ec
        )
        self.C_f = Factor(gid="C_f", scope_vars=set([self.C]), factor_fn=phi_c)
        self.FE_f = Factor(
            gid="FE_f", scope_vars=set([self.F, self.E]), factor_fn=phi_fe
        )
        self.DE_f = Factor(
            gid="DE_f", scope_vars=set([self.D, self.E]), factor_fn=phi_de
        )
        self.bayes_n = BayesianNetwork(
            gid="ba",
            nodes=set([self.C, self.E, self.D, self.F]),
            edges=set([self.EF, self.CE, self.ED]),
            factors=set([self.C_f, self.DE_f, self.CE_f, self.FE_f]),
        )

    def test_id(self):
        ""
        self.assertEqual("b", self.bayes.id())

    def test_conditional_inference(self):
        """!
        Test inference on bayesian network
        """
        query_vars = set([self.E])
        evidences = set([("F", True)])
        probs, alpha = self.bayes_n.cond_prod_by_variable_elimination(
            query_vars, evidences=evidences
        )
        for ps in probs.scope_products:
            pss = set(ps)
            ff = round(probs.phi(pss), 4)
            if set([("E", True)]) == pss:
                self.assertEqual(ff, 0.774)


if __name__ == "__main__":
    unittest.main()
