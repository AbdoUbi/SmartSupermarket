using System.IO;
using System;
using System.ComponentModel.DataAnnotations.Schema;
using System.Security.Policy;

namespace UserSignUp
{
    public partial class SmartSupermarket : Form
    {
        public SmartSupermarket()
        {
            InitializeComponent();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }

        private void SmartSupermarket_Load(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void textBox4_TextChanged(object sender, EventArgs e)
        {

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        string photopath = "";
        string FName_ = "";
        string LName_ = "";
        string Age_ = "";
        string CCN_ = "";
        string CCED_ = "";
        string CCV_ = "";
        int customerID = 0;
        private void button1_Click(object sender, EventArgs e)
        {
            OpenFileDialog file = new OpenFileDialog();
            file.Filter = "Jpegs|*.Jpegs|png|*.png|jpg|*.jpg";
            file.Title = "Please select an Image";
            if (file.ShowDialog() == DialogResult.OK)
            {
                photopath = file.FileName;
            }


        }

        private void button2_Click(object sender, EventArgs e)
        {
            FName_ = FName.Text;
            LName_ = LName.Text;
            Age_ = Age.Text;
            CCN_ = CCN.Text;
            CCED_ = CCED.Text;
            CCV_ = CCV.Text;
            customerID = Math.Abs(FName.GetHashCode() * DateTime.Now.GetHashCode());
            try
            {



                string path = Path.Combine(Directory.GetParent(Directory.GetCurrentDirectory()).ToString(), "USERS_DATABASE.csv");
                using (System.IO.StreamWriter file = new System.IO.StreamWriter(path, true))
                {
                    file.WriteLine(FName_ + ";" + LName_ + ";" + Age_ + ";" + CCN_ + ";" + CCED_ + ";" + CCV_ + ";" + customerID + ";" + photopath);
                    MessageBox.Show("Sign up Successful");
                    FName.Text = "";
                    LName.Text = "";
                    Age.Text = "";
                    CCN.Text = "";
                    CCED.Text = "";
                    CCV.Text = "";
                }
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error: ", ex);
            }

        }
    }
}