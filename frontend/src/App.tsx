import { useState, useEffect } from 'react';
import { Routes, Route, Link, useNavigate, useParams } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Button,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { huertoApi, cajonApi, cultivoApi, climaApi } from './services/api';
import type { Huerto, Cajon, Cultivo, Clima } from './types';

function App() {
  const [huertos, setHuertos] = useState<Huerto[]>([]);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHuertos = async () => {
      try {
        const response = await huertoApi.getAll();
        setHuertos(response.data);
      } catch (error) {
        console.error('Error al cargar huertos:', error);
      }
    };
    fetchHuertos();
  }, []);

  const toggleDrawer = (open: boolean) => (event: React.KeyboardEvent | React.MouseEvent) => {
    if (
      event.type === 'keydown' &&
      ((event as React.KeyboardEvent).key === 'Tab' ||
        (event as React.KeyboardEvent).key === 'Shift')
    ) {
      return;
    }
    setDrawerOpen(open);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="static" sx={{ bgcolor: '#4CAF50' }}>
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={toggleDrawer(true)}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Gestión de Huerto Urbano
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer anchor="left" open={drawerOpen} onClose={toggleDrawer(false)}>
        <Box
          sx={{ width: 250 }}
          role="presentation"
          onClick={toggleDrawer(false)}
          onKeyDown={toggleDrawer(false)}
        >
          <List>
            <ListItem disablePadding>
              <ListItemButton component={Link} to="/">
                <ListItemText primary="Inicio" />
              </ListItemButton>
            </ListItem>
            {huertos.map((huerto) => (
              <ListItem key={huerto.id} disablePadding>
                <ListItemButton
                  component={Link}
                  to={`/huerto/${huerto.id}`}
                >
                  <ListItemText primary={`Huerto: ${huerto.municipio}`} />
                </ListItemButton>
              </ListItem>
            ))}
            <ListItem disablePadding>
              <ListItemButton component={Link} to="/huertos/nuevo">
                <ListItemText primary="Nuevo Huerto" />
              </ListItemButton>
            </ListItem>
            <ListItem disablePadding>
              <ListItemButton component={Link} to="/cultivos">
                <ListItemText primary="Cultivos" />
              </ListItemButton>
            </ListItem>
            <ListItem disablePadding>
              <ListItemButton component={Link} to="/clima">
                <ListItemText primary="Clima (AEMET)" />
              </ListItemButton>
            </ListItem>
          </List>
        </Box>
      </Drawer>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/huerto/:id" element={<HuertoDetailPage />} />
          <Route path="/huerto/:id/cajones" element={<CajonesPage />} />
          <Route path="/huertos/nuevo" element={<NuevoHuertoPage />} />
          <Route path="/cultivos" element={<CultivosPage />} />
          <Route path="/cultivos/nuevo" element={<NuevoCultivoPage />} />
          <Route path="/clima" element={<ClimaPage />} />
        </Routes>
      </Container>
    </Box>
  );
}

function HomePage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Bienvenido a la Gestión de Huerto Urbano
      </Typography>
      <Typography variant="body1">
        Usa el menú lateral para navegar entre las diferentes secciones.
      </Typography>
    </Box>
  );
}

function HuertoDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [huerto, setHuerto] = useState<Huerto | null>(null);
  const [cajones, setCajones] = useState<Cajon[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (id) {
          const huertoResponse = await huertoApi.getById(Number(id));
          setHuerto(huertoResponse.data);
          const cajonesResponse = await cajonApi.getAll();
          setCajones(cajonesResponse.data.filter((c: Cajon) => c.huerto_id === Number(id)));
        }
      } catch (error) {
        console.error('Error al cargar datos del huerto:', error);
      }
    };
    fetchData();
  }, [id]);

  if (!huerto) {
    return <Typography>Cargando...</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Huerto: {huerto.municipio}
      </Typography>
      <Typography variant="body1" gutterBottom>
        Tipo: {huerto.tipo || 'No especificado'}
      </Typography>
      <Typography variant="body1" gutterBottom>
        Método de cultivo: {huerto.metodo_cultivo || 'No especificado'}
      </Typography>
      <Button
        variant="contained"
        color="primary"
        component={Link}
        to={`/huerto/${id}/cajones`}
        sx={{ mt: 2 }}
      >
        Ver Cajones
      </Button>
    </Box>
  );
}

function CajonesPage() {
  const { id } = useParams<{ id: string }>();
  const [cajones, setCajones] = useState<Cajon[]>([]);

  useEffect(() => {
    const fetchCajones = async () => {
      try {
        const response = await cajonApi.getAll();
        setCajones(response.data.filter((c: Cajon) => c.huerto_id === Number(id)));
      } catch (error) {
        console.error('Error al cargar cajones:', error);
      }
    };
    fetchCajones();
  }, [id]);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Cajones del Huerto
      </Typography>
      <Button
        variant="contained"
        color="primary"
        component={Link}
        to={`/huerto/${id}/cajones/nuevo`}
        sx={{ mb: 2 }}
      >
        Nuevo Cajón
      </Button>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Nombre</TableCell>
              <TableCell>Tipo</TableCell>
              <TableCell>Ubicación</TableCell>
              <TableCell>Exposición Solar (h)</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {cajones.map((cajon) => (
              <TableRow key={cajon.id}>
                <TableCell>{cajon.id}</TableCell>
                <TableCell>{cajon.nombre}</TableCell>
                <TableCell>{cajon.tipo}</TableCell>
                <TableCell>{cajon.ubicacion}</TableCell>
                <TableCell>{cajon.exposicion_solar}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

function NuevoHuertoPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<Omit<Huerto, 'id'>>({
    municipio: '',
    tipo: '',
    metodo_cultivo: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await huertoApi.create(formData);
      navigate('/');
    } catch (error) {
      console.error('Error al crear huerto:', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Typography variant="h4" gutterBottom>
        Nuevo Huerto
      </Typography>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 400 }}>
        <TextField
          label="Municipio"
          name="municipio"
          value={formData.municipio}
          onChange={handleChange}
          required
          fullWidth
        />
        <TextField
          label="Tipo (urbano, balcón, terraza)"
          name="tipo"
          value={formData.tipo}
          onChange={handleChange}
          fullWidth
        />
        <TextField
          label="Método de Cultivo (ecológico, convencional)"
          name="metodo_cultivo"
          value={formData.metodo_cultivo}
          onChange={handleChange}
          fullWidth
        />
        <Button type="submit" variant="contained" color="primary">
          Crear Huerto
        </Button>
      </Box>
    </Box>
  );
}

function CultivosPage() {
  const [cultivos, setCultivos] = useState<Cultivo[]>([]);

  useEffect(() => {
    const fetchCultivos = async () => {
      try {
        const response = await cultivoApi.getAll();
        setCultivos(response.data);
      } catch (error) {
        console.error('Error al cargar cultivos:', error);
      }
    };
    fetchCultivos();
  }, []);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Lista de Cultivos
      </Typography>
      <Button
        variant="contained"
        color="primary"
        component={Link}
        to="/cultivos/nuevo"
        sx={{ mb: 2 }}
      >
        Nuevo Cultivo
      </Button>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Nombre</TableCell>
              <TableCell>Familia Botánica</TableCell>
              <TableCell>Requisitos de Luz</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {cultivos.map((cultivo) => (
              <TableRow key={cultivo.id}>
                <TableCell>{cultivo.id}</TableCell>
                <TableCell>{cultivo.nombre}</TableCell>
                <TableCell>{cultivo.familia_botanica || 'N/A'}</TableCell>
                <TableCell>{cultivo.requisitos_luz || 'N/A'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

function NuevoCultivoPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<Omit<Cultivo, 'id'>>({
    nombre: '',
    familia_botanica: '',
    descripcion: '',
    requisitos_luz: '',
    requisitos_agua: '',
    temperatura_optima_min: undefined,
    temperatura_optima_max: undefined,
    ph_optimo_min: undefined,
    ph_optimo_max: undefined,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await cultivoApi.create(formData);
      navigate('/cultivos');
    } catch (error) {
      console.error('Error al crear cultivo:', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name.includes('temperatura') || name.includes('ph')
        ? value === '' ? undefined : Number(value)
        : value
    }));
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Typography variant="h4" gutterBottom>
        Nuevo Cultivo
      </Typography>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 400 }}>
        <TextField
          label="Nombre"
          name="nombre"
          value={formData.nombre}
          onChange={handleChange}
          required
          fullWidth
        />
        <TextField
          label="Familia Botánica"
          name="familia_botanica"
          value={formData.familia_botanica}
          onChange={handleChange}
          fullWidth
        />
        <TextField
          label="Descripción"
          name="descripcion"
          value={formData.descripcion}
          onChange={handleChange}
          fullWidth
          multiline
          rows={3}
        />
        <TextField
          label="Requisitos de Luz"
          name="requisitos_luz"
          value={formData.requisitos_luz}
          onChange={handleChange}
          fullWidth
        />
        <TextField
          label="Requisitos de Agua"
          name="requisitos_agua"
          value={formData.requisitos_agua}
          onChange={handleChange}
          fullWidth
        />
        <TextField
          label="Temperatura Óptima Mínima (°C)"
          name="temperatura_optima_min"
          type="number"
          value={formData.temperatura_optima_min || ''}
          onChange={handleChange}
          fullWidth
          InputLabelProps={{ shrink: true }}
        />
        <TextField
          label="Temperatura Óptima Máxima (°C)"
          name="temperatura_optima_max"
          type="number"
          value={formData.temperatura_optima_max || ''}
          onChange={handleChange}
          fullWidth
          InputLabelProps={{ shrink: true }}
        />
        <TextField
          label="pH Óptimo Mínimo"
          name="ph_optimo_min"
          type="number"
          value={formData.ph_optimo_min || ''}
          onChange={handleChange}
          fullWidth
          InputLabelProps={{ shrink: true }}
        />
        <TextField
          label="pH Óptimo Máximo"
          name="ph_optimo_max"
          type="number"
          value={formData.ph_optimo_max || ''}
          onChange={handleChange}
          fullWidth
          InputLabelProps={{ shrink: true }}
        />
        <Button type="submit" variant="contained" color="primary">
          Crear Cultivo
        </Button>
      </Box>
    </Box>
  );
}

function ClimaPage() {
  const [municipio, setMunicipio] = useState('madrid');
  const [climaData, setClimaData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchClimaAEMET = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await climaApi.getAEMET(municipio);
      setClimaData(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
      console.error('Error al obtener clima:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClimaAEMET();
  }, [municipio]);

  const handleMunicipioChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMunicipio(e.target.value);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Datos Climáticos (AEMET)
      </Typography>
      <Typography variant="body1" gutterBottom>
        Selecciona un municipio para ver los datos climáticos actuales.
      </Typography>
      
      <Box sx={{ display: 'flex', gap: 2, mb: 3, alignItems: 'center' }}>
        <TextField
          label="Municipio"
          value={municipio}
          onChange={handleMunicipioChange}
          select
          SelectProps={{ native: true }}
          sx={{ minWidth: 200 }}
        >
          <option value="madrid">Madrid</option>
          <option value="barcelona">Barcelona</option>
          <option value="valencia">Valencia</option>
          <option value="sevilla">Sevilla</option>
          <option value="bilbao">Bilbao</option>
          <option value="malaga">Málaga</option>
          <option value="zaragoza">Zaragoza</option>
          <option value="alicante">Alicante</option>
          <option value="cadiz">Cádiz</option>
          <option value="coruna">A Coruña</option>
        </TextField>
        <Button
          variant="contained"
          color="primary"
          onClick={fetchClimaAEMET}
          disabled={loading}
        >
          {loading ? 'Cargando...' : 'Actualizar Clima'}
        </Button>
      </Box>

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          Error: {error}
        </Typography>
      )}

      {climaData && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Atributo</TableCell>
                <TableCell>Valor</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>Municipio</TableCell>
                <TableCell>{climaData.municipio}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Fecha</TableCell>
                <TableCell>{climaData.fecha}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Temperatura Mínima (°C)</TableCell>
                <TableCell>{climaData.temperatura_min}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Temperatura Máxima (°C)</TableCell>
                <TableCell>{climaData.temperatura_max}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Humedad Relativa (%)</TableCell>
                <TableCell>{climaData.humedad_relativa}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Precipitación (mm)</TableCell>
                <TableCell>{climaData.precipitacion}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Velocidad del Viento (km/h)</TableCell>
                <TableCell>{climaData.velocidad_viento}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Dirección del Viento</TableCell>
                <TableCell>{climaData.direccion_viento}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Fuente</TableCell>
                <TableCell>{climaData.fuente}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
}

export default App;
