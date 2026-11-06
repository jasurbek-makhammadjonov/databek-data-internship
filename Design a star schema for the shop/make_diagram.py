import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

RH, HH = 0.42, 0.62  # row height, header height

def table(ax, x, top, w, title, rows, color, badge=None):
    h = HH + RH * len(rows)
    ax.add_patch(Rectangle((x, top - h), w, h, fc="white", ec="#333", lw=1.4, zorder=2))
    ax.add_patch(Rectangle((x, top - HH), w, HH, fc=color, ec="#333", lw=1.4, zorder=3))
    ax.text(x + 0.15, top - HH / 2, title, color="white", fontsize=12.5,
            fontweight="bold", va="center", zorder=4)
    if badge:
        ax.text(x + w - 0.15, top - HH / 2, badge, color="white", fontsize=10,
                fontweight="bold", va="center", ha="right", zorder=4)
    for i, (name, tag) in enumerate(rows):
        y = top - HH - RH * (i + 0.5)
        if i % 2 == 1:
            ax.add_patch(Rectangle((x, y - RH / 2), w, RH, fc="#F3F6FA", ec="none", zorder=2))
        ax.text(x + 0.15, y, name, fontsize=10, va="center", zorder=4,
                fontweight="bold" if tag in ("PK",) else "normal")
        if tag:
            ax.text(x + w - 0.15, y, tag, fontsize=9, va="center", ha="right",
                    color="#B03A2E" if tag == "FK" else "#1F4E79", fontweight="bold", zorder=4)
    return dict(x=x, top=top, w=w, h=h, bottom=top - h,
                row_y=lambda i: top - HH - RH * (i + 0.5))

def link(ax, p1, p2, l1="1", l2="N"):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#555", lw=1.6, zorder=1)
    for (px, py), qx, qy, lab in ((p1, p2[0], p2[1], l1), (p2, p1[0], p1[1], l2)):
        dx, dy = qx - px, qy - py
        n = (dx**2 + dy**2) ** 0.5
        ax.text(px + dx / n * 0.35, py + dy / n * 0.35 + 0.12, lab, fontsize=11,
                fontweight="bold", color="#222", ha="center", zorder=5,
                bbox=dict(fc="white", ec="none", pad=0.5))

fig, ax = plt.subplots(figsize=(20, 13))
ax.set_xlim(0, 20); ax.set_ylim(0, 13); ax.axis("off")

ax.text(10, 12.55, "Star Schema: Online Shop (shop.db)", fontsize=22,
        fontweight="bold", ha="center")
ax.text(10, 12.1, "Source: customers, products, orders, order_items  ->  1 fact table + 4 dimensions",
        fontsize=12, ha="center", color="#555")

fact = table(ax, 7.4, 9.0, 5.2, "fact_order_items", [
    ("order_item_key", "PK"), ("order_id (degenerate dim)", ""),
    ("customer_key", "FK"), ("product_key", "FK"), ("date_key", "FK"), ("status_key", "FK"),
    ("quantity", ""), ("unit_price", ""), ("line_amount = qty x price", "")], "#1F4E79")

cust = table(ax, 0.5, 11.8, 5.4, "dim_customer", [
    ("customer_key", "PK"), ("customer_id", "NK"), ("name", ""), ("email", ""),
    ("city", ""), ("signup_date", ""), ("valid_from", ""), ("valid_to", ""),
    ("is_current", "")], "#1E8449", "SCD Type 2")

prod = table(ax, 14.1, 11.8, 5.4, "dim_product", [
    ("product_key", "PK"), ("product_id", "NK"), ("name", ""), ("category", ""),
    ("list_price", ""), ("valid_from", ""), ("valid_to", ""), ("is_current", "")],
    "#B9770E", "SCD Type 2")

date = table(ax, 0.5, 6.4, 5.4, "dim_date", [
    ("date_key (YYYYMMDD)", "PK"), ("full_date", ""), ("year", ""), ("quarter", ""),
    ("month", ""), ("month_name", ""), ("day", ""), ("day_of_week", ""),
    ("is_weekend", "")], "#7D3C98", "SCD Type 0")

stat = table(ax, 14.1, 6.4, 5.4, "dim_order_status", [
    ("status_key", "PK"), ("status_name", ""), ("is_revenue", "")],
    "#C0392B", "SCD Type 1")

fx0, fx1 = fact["x"], fact["x"] + fact["w"]
link(ax, (cust["x"] + cust["w"], cust["row_y"](0) - 1.0), (fx0, fact["row_y"](2)))
link(ax, (prod["x"], prod["row_y"](0) - 1.0), (fx1, fact["row_y"](3)))
link(ax, (date["x"] + date["w"], date["row_y"](0)), (fx0, fact["row_y"](4)))
link(ax, (stat["x"], stat["row_y"](0)), (fx1, fact["row_y"](5)))

# grain box
ax.add_patch(FancyBboxPatch((7.2, 2.35), 5.6, 1.85, boxstyle="round,pad=0.05",
                            fc="#FFF8E1", ec="#B9770E", lw=1.6, zorder=2))
ax.text(10, 3.85, "GRAIN", fontsize=12, fontweight="bold", ha="center", color="#B9770E")
ax.text(10, 3.2, "One row = one product line\nof one order (one order_items row)",
        fontsize=12, ha="center", va="center")
ax.text(10, 2.65, "Measures: quantity, unit_price, line_amount", fontsize=10,
        ha="center", color="#555")

# SCD legend
ax.add_patch(FancyBboxPatch((0.5, 0.15), 19, 1.7, boxstyle="round,pad=0.05",
                            fc="#F8F9F9", ec="#999", lw=1.2, zorder=2))
lines = [
    ("dim_customer", "Type 2", "city/email can change; old orders must keep the city the customer had at purchase time."),
    ("dim_product", "Type 2", "category and list price change over time; history is needed for price/category analysis."),
    ("dim_date", "Type 0", "a calendar date never changes."),
    ("dim_order_status", "Type 1", "tiny lookup; a label fix just overwrites, no history needed."),
]
for i, (d, t, r) in enumerate(lines):
    y = 1.58 - i * 0.37
    ax.text(0.8, y, d, fontsize=10.5, fontweight="bold", va="center")
    ax.text(3.6, y, t, fontsize=10.5, fontweight="bold", va="center", color="#1F4E79")
    ax.text(4.7, y, r, fontsize=10.5, va="center")

ax.text(19.6, 12.1, "PK primary key   FK foreign key   NK natural key   1 / N cardinality",
        fontsize=9.5, ha="right", color="#555")

plt.savefig("star_schema.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.savefig("star_schema.pdf", bbox_inches="tight", facecolor="white")
print("ok")
