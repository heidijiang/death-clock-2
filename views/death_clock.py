"""Death clock generator and renderer."""
import base64
import calendar
import datetime
import io

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

COLOR = "w"
DEFAULT_AGE = 38

mpl.rcParams["text.color"] = COLOR
mpl.rcParams["axes.labelcolor"] = COLOR
mpl.rcParams["xtick.color"] = COLOR
mpl.rcParams["ytick.color"] = COLOR
mpl.rcParams["figure.facecolor"] = "k"
mpl.rcParams["axes.facecolor"] = "k"
mpl.rcParams["savefig.facecolor"] = "k"
mpl.rcParams["font.family"] = "Andale Mono"


class DeathdayGenerator:
    """Get the deathdate given a name and age."""

    def __init__(self, name: str, data: pd.DataFrame, age: int):
        "Initialize."
        self.name = name
        self.age = age
        self.max_age = data["age"].max()
        self.today = datetime.date.today()
        self.dob = self.get_dob()
        self.death_date = None
        self.death_age = None

    def get_dob(self):
        """Get dob of user."""
        self.check_age()
        return datetime.date(
            self.today.year - self.age, self.today.month, self.today.day
        )

    def check_age(self) -> None:
        """Check to make sure age is valid."""
        if self.age >= self.max_age or self.age <= 0:
            self.age = DEFAULT_AGE

    def _adjust_dist_wrt_age(self, data: pd.DataFrame) -> pd.DataFrame:
        """Adjust distribution relative to age of user."""
        data_w_age = data[data["age"] > self.age].copy().reset_index()
        data_w_age["pdata"] = data_w_age["all"] / data_w_age["all"].sum() * 100
        data_w_age["cdata"] = data_w_age["pdata"].cumsum() * 100

        yr_diff = data_w_age["age"].max() - data_w_age["age"].min() + 1
        data_w_age["year"] = np.arange(self.today.year, self.today.year + yr_diff)
        return data_w_age

    def draw_age_of_death(self, data: pd.DataFrame) -> None:
        """Randomly draw from distribution to determine age of death."""
        adj_data = self._adjust_dist_wrt_age(data)
        r_float = np.random.random(1)[0]
        idx = (adj_data["cdata"] - r_float).abs().idxmin()
        if r_float >= adj_data["cdata"].iloc[idx]:
            idx += 1
        self.death_age = adj_data["age"].iloc[idx]

    def _draw_random_date(self, year) -> None:
        """Get random date from today on."""
        if year == self.today.year:
            start_date = self.today.toordinal()
        else:
            start_date = datetime.date(year, 1, 1).toordinal()
        end_date = datetime.date(year, 12, 31).toordinal()
        return datetime.date.fromordinal(np.random.randint(start_date, end_date))

    def get_death_date(self, data: pd.DataFrame):
        """Get death date."""
        self.draw_age_of_death(data)
        death_year = self.dob.year + self.death_age
        self.death_date = self._draw_random_date(death_year)

    def printed_date(self):
        """Printed version of death date."""
        if self.death_date:
            months = [i for i in calendar.month_abbr]
            month = months[self.death_date.month]
            return f"{month} {self.death_date.day}, {self.death_date.year}"
        return "Deathday not calculated yet!"

    def save_display(self, data):
        """Display."""
        _, axes = plt.subplots(1, 2, figsize=(10, 4))
        data = self._adjust_dist_wrt_age(data)
        sns.lineplot(data=data, x="year", y="pdata", ax=axes[0], color="pink")
        axes[0].scatter(
            self.death_date.year,
            data.loc[data["year"] == self.death_date.year, "pdata"],
            c="red",
        )
        axes[0].set_ylabel("Probability of death")
        sns.lineplot(data=data, x="year", y="cdata", ax=axes[1], color="pink")
        axes[1].scatter(
            self.death_date.year,
            data.loc[data["year"] == self.death_date.year, "cdata"],
            c="red",
        )
        axes[1].set_ylabel("Cumulative probability of death")
        for axis in axes:
            axis.spines["bottom"].set_color(COLOR)
            axis.spines["top"].set_color(COLOR)
            axis.spines["left"].set_color(COLOR)
            axis.spines["right"].set_color(COLOR)
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return f"data:image/png;base64,{graph_url}"
