import numpy as np  #pseudo math tools
import pandas as pd  #pseudo data table
import matplotlib.pyplot as plt  #pseudo charts

from sklearn.model_selection import train_test_split  #pseudo split data
from sklearn.compose import ColumnTransformer  #pseudo prep builder
from sklearn.pipeline import Pipeline  #pseudo steps chain
from sklearn.preprocessing import OneHotEncoder  #pseudo text to numbers
from sklearn.impute import SimpleImputer  #pseudo fill blanks
from sklearn.metrics import confusion_matrix  #pseudo error counts

from sklearn.linear_model import LogisticRegression  #pseudo model 1
from sklearn.ensemble import RandomForestClassifier  #pseudo model 2

lab = pd.read_csv("websites_labelled.csv")  #pseudo load training
tst = pd.read_csv("websites_unlabelled.csv")  #pseudo load testing

lab.columns = [c.strip() for c in lab.columns]  #pseudo clean names
tst.columns = [c.strip() for c in tst.columns]  #pseudo clean names

lab["label"] = lab["label"].astype(str).str.strip().str.lower()  #pseudo normalize label
lab = lab[lab["label"].isin(["good","bad"])].copy()  #pseudo keep valid rows
lab["y"] = (lab["label"] == "bad").astype(int)  #pseudo bad=1 good=0

m = (lab["website_exist_time"] < 100)  #pseudo legal rule flag
lab.loc[m, "registered_domain"] = "Unknown"  #pseudo hide whois
m = (tst["website_exist_time"] < 100)  #pseudo legal rule flag
tst.loc[m, "registered_domain"] = "Unknown"  #pseudo hide whois

lab.loc[lab["js_obf_len"] > 100, "y"] = 1  #pseudo auto-bad rule

plt.figure()  #pseudo new chart
lab["y"].replace({0:"good",1:"bad"}).value_counts().plot(kind="bar")  #pseudo count bars
plt.title("Training labels")  #pseudo title
plt.tight_layout()  #pseudo fit
plt.savefig("labels.png", dpi=160)  #pseudo save

plt.figure()  #pseudo new chart
lab.boxplot(column="js_obf_len", by="y")  #pseudo compare by class
plt.title("js_obf_len vs label")  #pseudo title
plt.suptitle("")  #pseudo remove extra title
plt.tight_layout()  #pseudo fit
plt.savefig("js_obf_len_box.png", dpi=160)  #pseudo save

X = lab.drop(columns=["label","y"], errors="ignore")  #pseudo features
y = lab["y"].copy()  #pseudo target

num = X.select_dtypes(include=["int64","float64"]).columns.tolist()  #pseudo numeric cols
cat = [c for c in X.columns if c not in num]  #pseudo text cols
if "unique_id" in num: num.remove("unique_id")  #pseudo drop id
if "unique_id" in cat: cat.remove("unique_id")  #pseudo drop id

prep = ColumnTransformer([  #pseudo build prep
    ("n", Pipeline([("imp", SimpleImputer(strategy="median"))]), num),  #pseudo fill nums
    ("c", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat)  #pseudo fill+encode cats
])  #pseudo end prep

Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)  #pseudo split

C_FN = 1000  #pseudo breach cost
C_FP = 50  #pseudo review cost

def best_t(y_true, p_bad):  #pseudo pick cutoff
    best = (1e18, 0.5, None)  #pseudo (cost, t, cm)
    for t in np.linspace(0.01, 0.99, 99):  #pseudo try many t
        pred = (p_bad >= t).astype(int)  #pseudo apply t
        tn, fp, fn, tp = confusion_matrix(y_true, pred, labels=[0,1]).ravel()  #pseudo counts
        cost = fn*C_FN + fp*C_FP  #pseudo total cost
        if cost < best[0]: best = (cost, t, (tn, fp, fn, tp))  #pseudo keep best
    return best  #pseudo done

m1 = Pipeline([("p", prep), ("m", LogisticRegression(max_iter=2000))])  #pseudo model 1 pipe
m2 = Pipeline([("p", prep), ("m", RandomForestClassifier(n_estimators=300, random_state=42, class_weight="balanced"))])  #pseudo model 2 pipe

m1.fit(Xtr, ytr)  #pseudo train m1
p1 = m1.predict_proba(Xva)[:,1]  #pseudo prob bad
r1 = best_t(yva.values, p1)  #pseudo best threshold

m2.fit(Xtr, ytr)  #pseudo train m2
p2 = m2.predict_proba(Xva)[:,1]  #pseudo prob bad
r2 = best_t(yva.values, p2)  #pseudo best threshold

win = ("LogReg", m1, r1) if r1[0] <= r2[0] else ("RandForest", m2, r2)  #pseudo choose winner
name, model, (cost, tstar, cm) = win  #pseudo unpack

model.fit(X, y)  #pseudo refit on all training
p_bad = model.predict_proba(tst)[:,1]  #pseudo test probs
pred = np.where(p_bad >= tstar, "bad", "good")  #pseudo final labels

uid = tst["unique_id"] if "unique_id" in tst.columns else pd.Series(np.arange(len(tst)))  #pseudo ids
out = pd.DataFrame({"unique_id": uid, "prob_bad": p_bad, "predicted_label": pred})  #pseudo output table
out.to_csv("predictions.csv", index=False)  #pseudo save predictions

tn, fp, fn, tp = cm  #pseudo unpack confusion
with open("results_summary.txt","w",encoding="utf-8") as f:  #pseudo write summary
    f.write(f"winner={name}\n")  #pseudo winner
    f.write(f"threshold={tstar:.2f}\n")  #pseudo cutoff
    f.write(f"cost_fn={C_FN} cost_fp={C_FP}\n")  #pseudo costs
    f.write(f"tn={tn} fp={fp} fn={fn} tp={tp}\n")  #pseudo counts
    f.write(f"total_cost={cost}\n")  #pseudo total cost

print("done -> predictions.csv, results_summary.txt, labels.png, js_obf_len_box.png")  #pseudo finish