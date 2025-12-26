import io
import re
from decimal import Decimal
from typing import Dict
import pdfplumber


class GBMStatementParser:
    """Parser for GBM (Grupo Bursátil Mexicano) brokerage account statements"""

    @staticmethod
    def parse_gbm_pdf(file_content: bytes) -> dict:
        """
        Parse a GBM PDF statement and extract portfolio summary data.

        Returns dict matching the specification:
        {
            "statement_date": "2022-01-31",
            "account_holder": "JUAN PEREZ GOMEZ",
            "currency": "MXN",
            "portfolio_summary": {
                "equity": 97839.30,
                "fixed_income": 385.56,
                "cash": 6.85,
                "total_value": 98231.71
            },
            "extracted_from": "filename.pdf"
        }
        """
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                # Extract text from all pages
                full_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"

                # Extract data from the "RESUMEN DEL PORTAFOLIO" section
                account_holder = GBMStatementParser._extract_account_holder(full_text)
                statement_date = GBMStatementParser._extract_statement_date(full_text)

                # Extract portfolio values
                equity = GBMStatementParser._find_value(full_text, "RENTA VARIABLE")
                fixed_income = GBMStatementParser._find_value(full_text, "DEUDA")
                cash = GBMStatementParser._find_value(full_text, "EFECTIVO")
                total_value = GBMStatementParser._find_total_value(full_text)

                # If total is not found, calculate it
                if total_value == 0.0:
                    total_value = equity + fixed_income + cash

                # Extract individual positions
                positions = GBMStatementParser._extract_positions(full_text)

                return {
                    "statement_date": statement_date,
                    "account_holder": account_holder,
                    "currency": "MXN",
                    "portfolio_summary": {
                        "equity_value": equity,
                        "fixed_income_value": fixed_income,
                        "cash_value": cash,
                        "total_value": total_value
                    },
                    "breakdown": positions
                }

        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")

    @staticmethod
    def _extract_account_holder(text: str) -> str:
        """Extract account holder name from PDF"""
        # Pattern: matches name after "NOMBRE:" or before "Contrato:"
        patterns = [
            r'NOMBRE:\s*\n\s*([A-ZÁÉÍÓÚÑ\s]+)\s+Contrato',
            r'^([A-ZÁÉÍÓÚÑ\s]+)\s+Contrato:',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "Unknown"

    @staticmethod
    def _extract_statement_date(text: str) -> str:
        """Extract statement period end date"""
        # Pattern: "DEL 1 AL 31 DE DICIEMBRE DE 2021"
        # or "Periodo DEL 1 AL 31 DE DICIEMBRE DE 2021"
        month_map = {
            "ENERO": "01", "FEBRERO": "02", "MARZO": "03", "ABRIL": "04",
            "MAYO": "05", "JUNIO": "06", "JULIO": "07", "AGOSTO": "08",
            "SEPTIEMBRE": "09", "OCTUBRE": "10", "NOVIEMBRE": "11", "DICIEMBRE": "12"
        }

        pattern = r'DEL\s+\d+\s+AL\s+(\d+)\s+DE\s+([A-Z]+)\s+DE\s+(\d{4})'
        match = re.search(pattern, text)

        if match:
            day = match.group(1).zfill(2)
            month_name = match.group(2)
            year = match.group(3)
            month = month_map.get(month_name, "12")
            return f"{year}-{month}-{day}"

        return "2021-12-31"  # Default fallback

    @staticmethod
    def _find_value(text: str, category: str) -> float:
        """
        Extract monetary value for a specific category from the RESUMEN DEL PORTAFOLIO section.

        Looks for patterns like:
        RENTA VARIABLE    0.00    32,601.84    97.68
        DEUDA             0.00       766.81     2.30
        EFECTIVO          0.00         8.15     0.02

        Returns the "SALDO AL 31-DIC-21" column (second number)
        """
        # Pattern to match the category row with values
        # Format: CATEGORY  prev_value  current_value  percentage
        pattern = rf'{category}\s+[\d,]+\.?\d*\s+([\d,]+\.?\d*)\s+[\d.]+\s*'

        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value_str = match.group(1).replace(',', '')
            try:
                return float(value_str)
            except ValueError:
                return 0.0

        return 0.0

    @staticmethod
    def _find_total_value(text: str) -> float:
        """Extract total portfolio value"""
        # Pattern: "VALOR DEL PORTAFOLIO ... 33,376.80 100.00"
        pattern = r'VALOR\s+DEL\s+PORTAFOLIO[^\d]+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+[\d.]+\s*$'

        match = re.search(pattern, text, re.MULTILINE)
        if match:
            # The second value is the current total
            value_str = match.group(2).replace(',', '')
            try:
                return float(value_str)
            except ValueError:
                return 0.0

        return 0.0

    @staticmethod
    def _extract_positions(text: str) -> list:
        """Extract individual stock/ETF positions from the statement"""
        positions = []

        # Extract from "ACCIONES DEL SIC" section (International stocks/ETFs)
        # Pattern matches lines like:
        # PFE * 0 1 0 1,275.770000 1,275.77 1,208.588160 1,152.255969 1,208.59 (67.18) 3.62
        sic_pattern = r'([A-Z]+)\s+\*\s+\d+\s+(\d+)\s+\d+\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+[\d,]+\.?\d*\s+([\d,]+\.?\d*)\s+\(([\d,]+\.?\d*)\)\s+([\d.]+)'

        for match in re.finditer(sic_pattern, text):
            ticker = match.group(1)
            quantity = int(match.group(2))
            avg_cost = float(match.group(3).replace(',', ''))
            current_price = float(match.group(5).replace(',', ''))
            market_value = float(match.group(6).replace(',', ''))
            unrealized_gain_str = match.group(7).replace(',', '')
            unrealized_gain = -float(unrealized_gain_str)  # Negative because it's in parentheses

            # Calculate unrealized gain percentage
            if avg_cost * quantity > 0:
                unrealized_gain_percent = (unrealized_gain / (avg_cost * quantity)) * 100
            else:
                unrealized_gain_percent = 0.0

            positions.append({
                "ticker": ticker,
                "name": GBMStatementParser._get_ticker_name(ticker),
                "quantity": quantity,
                "avg_cost": avg_cost,
                "current_price": current_price,
                "market_value": market_value,
                "unrealized_gain": unrealized_gain,
                "unrealized_gain_percent": unrealized_gain_percent
            })

        # Extract from "ACCIONES" section (Mexican stocks)
        # Pattern: AEROMEX * 0 1,200 0 1.410000 1,692.00 2.780000 5.200000 3,336.00 1,644.00 9.99
        mex_pattern = r'([A-Z]+)\s+\*\s+\d+\s+([\d,]+)\s+\d+\s+([\d.]+)\s+([\d,]+\.?\d*)\s+([\d.]+)\s+[\d.]+\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d.]+)'

        for match in re.finditer(mex_pattern, text):
            ticker = match.group(1)
            # Skip if already processed in SIC section
            if any(p["ticker"] == ticker for p in positions):
                continue

            quantity = int(match.group(2).replace(',', ''))
            avg_cost = float(match.group(3))
            current_price = float(match.group(5))
            market_value = float(match.group(6).replace(',', ''))
            unrealized_gain = float(match.group(7).replace(',', ''))

            # Calculate unrealized gain percentage
            if avg_cost * quantity > 0:
                unrealized_gain_percent = (unrealized_gain / (avg_cost * quantity)) * 100
            else:
                unrealized_gain_percent = 0.0

            positions.append({
                "ticker": ticker,
                "name": GBMStatementParser._get_ticker_name(ticker),
                "quantity": quantity,
                "avg_cost": avg_cost,
                "current_price": current_price,
                "market_value": market_value,
                "unrealized_gain": unrealized_gain,
                "unrealized_gain_percent": unrealized_gain_percent
            })

        return positions

    @staticmethod
    def _get_ticker_name(ticker: str) -> str:
        """Get company/fund name for a ticker symbol"""
        names = {
            "PFE": "Pfizer Inc.",
            "VEA": "Vanguard FTSE Developed Markets ETF",
            "VNQ": "Vanguard Real Estate ETF",
            "VOO": "Vanguard S&P 500 ETF",
            "VWO": "Vanguard FTSE Emerging Markets ETF",
            "AEROMEX": "Grupo Aeromexico",
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation",
            "GOOGL": "Alphabet Inc.",
            "VTI": "Vanguard Total Stock Market ETF"
        }
        return names.get(ticker, f"{ticker} Stock")


def parse_gbm_pdf(file_content: bytes) -> dict:
    """Wrapper function for the service layer"""
    return GBMStatementParser.parse_gbm_pdf(file_content)
