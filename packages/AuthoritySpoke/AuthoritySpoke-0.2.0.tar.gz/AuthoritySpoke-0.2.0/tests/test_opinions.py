import pytest

from authorityspoke.entities import Entity
from authorityspoke.io import loaders, readers
from authorityspoke.opinions import Opinion


class TestOpinions:
    def test_load_opinion_in_Harvard_format(self):
        watt_dict = loaders.load_opinion("watt_h.json")
        assert watt_dict.name_abbreviation == "Wattenburg v. United States"

    def test_load_generator_for_opinions(self):
        opinion_generator = iter(loaders.load_opinion("brad_h.json", lead_only=False))
        _ = next(opinion_generator)  # majority
        dissent = next(opinion_generator)
        assert dissent.position == "concurring-in-part-and-dissenting-in-part"

    def test_opinion_features(self, make_opinion):
        assert make_opinion["watt_majority"].court == "9th-cir"
        assert "388 F.2d 853" in make_opinion["watt_majority"].citations

    def test_repr(self, make_opinion):
        assert "HAMLEY, Circuit Judge" in repr(make_opinion["watt_majority"])

    def test_repr_excludes_text(self, make_opinion):
        """
        reprs would be way too long if they could contain the
        full opinion text.
        """
        assert "text" not in repr(make_opinion["watt_majority"])

    def test_opinion_author(self, make_opinion):
        assert make_opinion["watt_majority"].author == "HAMLEY, Circuit Judge"
        assert make_opinion["brad_majority"].author == "BURKE, J."
        assert (
            make_opinion["brad_concurring-in-part-and-dissenting-in-part"].author
            == "TOBRINER, J."
        )

    def test_opinion_text(self, make_opinion):
        assert (
            "Feist responded that such efforts were economically "
            + "impractical and, in any event, unnecessary"
        ) in make_opinion["feist_majority"].text

    def test_opinion_holding_list(
        self, make_opinion, real_holding, make_evidence, make_entity
    ):
        watt = make_opinion["watt_majority"]
        h = real_holding
        h3_specific = h["h3"]
        watt.posit(h3_specific)
        assert h3_specific in watt.holdings

    def test_opinion_text_anchor(self, make_opinion_with_holding):
        feist = make_opinion_with_holding["feist_majority"]
        assert any(
            "generally" in anchor for anchor in feist.get_anchors(feist.holdings[1])
        )

    def test_opinion_factor_text_anchor(self, make_opinion_with_holding):
        feist = make_opinion_with_holding["feist_majority"]
        assert all(
            "No one may claim originality" not in anchor
            for anchor in feist.get_anchors(feist.holdings[0])
        )
        assert any(
            "as to facts" in anchor for anchor in feist.get_anchors(feist.holdings[0])
        )

    def test_opinion_entity_list(
        self, make_opinion, real_holding, make_entity, make_evidence
    ):
        watt = make_opinion["watt_majority"]
        h = real_holding
        e = make_entity

        watt.posit(h["h1"], context=(e["motel"], e["watt"]))
        watt.posit(h["h2"], context=(e["trees"], e["motel"]))
        watt.posit(
            h["h3"],
            context=(
                make_evidence["generic"],
                e["motel"],
                e["watt"],
                e["trees"],
                e["tree_search"],
            ),
        )
        watt.posit(
            h["h4"], context=(e["trees"], e["tree_search"], e["motel"], e["watt"])
        )
        assert make_entity["watt"] in make_opinion["watt_majority"].generic_factors

    def test_opinion_date(self, make_opinion):
        assert (
            make_opinion["watt_majority"].decision_date
            < make_opinion["brad_majority"].decision_date
        )
        assert (
            make_opinion["brad_majority"].decision_date
            == make_opinion[
                "brad_concurring-in-part-and-dissenting-in-part"
            ].decision_date
        )

    def test_positing_non_rule_error(self, make_opinion, make_procedure):
        with pytest.raises(TypeError):
            make_opinion["watt_majority"].posit(make_procedure["c1"])

    def test_error_posit_with_no_rule_source(self, make_opinion):
        with pytest.raises(TypeError):
            make_opinion["watt_majority"].posit()

    def test_new_context_non_iterable_changes(self, make_opinion, make_holding):
        """
        The context here (a Factor outside an iterable) only changes the first
        generic factor of the Rule being posited, which may not be what the user
        expects.
        """
        brad = make_opinion["brad_majority"]
        brad.posit(make_holding["h1"], context=Entity("House on Haunted Hill"))
        assert "Haunted Hill" in str(brad.holdings[0])

    def test_new_context_naming_nonexistent_factor(self, make_opinion, make_holding):
        """
        The context here (a Factor outside an iterable) only changes the first
        generic factor of the Rule being posited, which may not be what the user
        expects.
        """
        brad = make_opinion["brad_majority"]
        with pytest.raises(ValueError):
            brad.posit(
                make_holding["h1"],
                context=(Entity("House on Haunted Hill"), "nonexistent factor"),
            )

    def test_new_context_creates_equal_rule(self, make_opinion, make_regime):
        watt = make_opinion["watt_majority"]
        brad = make_opinion["brad_majority"]
        # Clearing in case prior tests added holdings
        watt.holdings = []
        brad.holdings = []
        watt.posit(loaders.load_holdings("holding_watt.json", regime=make_regime))
        brad.posit(loaders.load_holdings("holding_brad.json", regime=make_regime))
        context_pairs = {
            "proof of Bradley's guilt": "proof of Wattenburg's guilt",
            "Bradley": "Wattenburg",
            "officers' search of the yard": "officers' search of the stockpile",
            "Bradley's marijuana patch": "the stockpile of trees",
        }
        watt.posit(brad.holdings[0], context_pairs)
        assert watt.holdings[-1].means(brad.holdings[0])

    def test_new_context_inferring_factors_to_change(self, make_opinion, make_regime):
        """
        This changes watt's holdings; may break tests below.
        """

        watt = make_opinion["watt_majority"]
        brad = make_opinion["brad_majority"]
        watt.holdings = []
        brad.holdings = []
        watt.posit(loaders.load_holdings("holding_watt.json", regime=make_regime))
        brad.posit(loaders.load_holdings("holding_brad.json", regime=make_regime))

        context_items = [
            "proof of Wattenburg's guilt",
            "Wattenburg",
            "officers' search of the stockpile",
            "Hideaway Lodge",
            "the stockpile of trees",
        ]
        watt.posit(brad.holdings[0], context=context_items)
        assert watt.holdings[-1].means(brad.holdings[0])


class TestImplication:
    def test_no_implication(self, make_opinion_with_holding):
        watt = make_opinion_with_holding["watt_majority"]
        brad = make_opinion_with_holding["brad_majority"]
        assert not watt >= brad

    def test_posit_list_of_holdings_and_imply(self, make_opinion, make_regime):
        watt = make_opinion["watt_majority"]
        brad = make_opinion["brad_majority"]
        some_rules = loaders.load_holdings(
            filename="holding_watt.json", regime=make_regime
        )
        for case in (watt, brad):
            case.holdings = []
            case.posit(some_rules[:3])
        watt.posit(some_rules[3])
        assert watt > brad
        assert not brad >= watt

    def test_opinion_implies_rule(self, make_opinion, make_holding):
        watt = make_opinion["watt_majority"]
        watt.holdings = [make_holding["h2_invalid_undecided"]]
        assert watt >= make_holding["h2_undecided"]
        assert watt > make_holding["h2_undecided"]

    def test_opinion_does_not_imply_rule(self, make_opinion, make_holding):
        watt = make_opinion["watt_majority"]
        watt.holdings = [make_holding["h2_irrelevant_inputs_undecided"]]
        assert not watt >= make_holding["h2_undecided"]
        assert not watt > make_holding["h2_undecided"]


class TestContradiction:
    def test_contradiction_of_holding(
        self, make_opinion_with_holding, make_enactment, make_holding
    ):
        assert make_opinion_with_holding["watt_majority"].contradicts(
            make_holding["h2_output_false_ALL_MUST"] + make_enactment["search_clause"]
        )

    def test_error_contradiction_with_procedure(self, make_opinion, make_procedure):
        with pytest.raises(TypeError):
            make_opinion["watt_majority"].contradicts(make_procedure["c1"])
