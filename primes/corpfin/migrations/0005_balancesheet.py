# Generated by Django 5.1.6 on 2025-02-17 14:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("corpfin", "0004_rename_filing_date_incomestatement_filling_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="BalanceSheet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("symbol", models.CharField(max_length=5)),
                ("reported_currency", models.CharField(max_length=3)),
                ("cik", models.CharField(max_length=10)),
                ("filling_date", models.DateField()),
                ("accepted_date", models.DateTimeField()),
                ("calendar_year", models.CharField(max_length=4)),
                ("period", models.CharField(max_length=2)),
                ("cash_and_cash_equivalents", models.BigIntegerField()),
                ("short_term_investments", models.BigIntegerField()),
                ("cash_and_short_term_investments", models.BigIntegerField()),
                ("net_receivables", models.BigIntegerField()),
                ("inventory", models.BigIntegerField()),
                ("other_current_assets", models.BigIntegerField()),
                ("total_current_assets", models.BigIntegerField()),
                ("property_plant_equipment_net", models.BigIntegerField()),
                ("goodwill", models.BigIntegerField()),
                ("intangible_assets", models.BigIntegerField()),
                ("goodwill_and_intangible_assets", models.BigIntegerField()),
                ("long_term_investments", models.BigIntegerField()),
                ("tax_assets", models.BigIntegerField()),
                ("other_non_current_assets", models.BigIntegerField()),
                ("total_non_current_assets", models.BigIntegerField()),
                ("other_assets", models.BigIntegerField()),
                ("total_assets", models.BigIntegerField()),
                ("account_payables", models.BigIntegerField()),
                ("short_term_debt", models.BigIntegerField()),
                ("tax_payables", models.BigIntegerField()),
                ("deferred_revenue", models.BigIntegerField()),
                ("other_current_liabilities", models.BigIntegerField()),
                ("total_current_liabilities", models.BigIntegerField()),
                ("long_term_debt", models.BigIntegerField()),
                ("deferred_revenue_non_current", models.BigIntegerField()),
                ("deferred_tax_liabilities_non_current", models.BigIntegerField()),
                ("other_non_current_liabilities", models.BigIntegerField()),
                ("total_non_current_liabilities", models.BigIntegerField()),
                ("other_liabilities", models.BigIntegerField()),
                ("capital_lease_obligations", models.BigIntegerField()),
                ("total_liabilities", models.BigIntegerField()),
                ("preferred_stock", models.BigIntegerField()),
                ("common_stock", models.BigIntegerField()),
                ("retained_earnings", models.BigIntegerField()),
                (
                    "accumulated_other_comprehensive_income_loss",
                    models.BigIntegerField(),
                ),
                ("other_total_stockholders_equity", models.BigIntegerField()),
                ("total_stockholders_equity", models.BigIntegerField()),
                ("total_equity", models.BigIntegerField()),
                ("total_liabilities_and_stockholders_equity", models.BigIntegerField()),
                ("minority_interest", models.BigIntegerField()),
                ("total_liabilities_and_total_equity", models.BigIntegerField()),
                ("total_investments", models.BigIntegerField()),
                ("total_debt", models.BigIntegerField()),
                ("net_debt", models.BigIntegerField()),
                ("link", models.URLField()),
                ("final_link", models.URLField()),
            ],
        ),
    ]
